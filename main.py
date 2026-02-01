import os
import time
import io
import threading
import telebot
import shutil
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN_TELEGRAM = "TOKEN_TELEGRAM"
CHATS_ID_TELEGRAM = set()
bot = telebot.TeleBot(TOKEN_TELEGRAM)

backup_lock = threading.Lock()

def autenticar():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    print("\nUsuário autenticado.")
    return build('drive', 'v3', credentials=creds)


def baixar_arquivo(service, file_id, caminho_destino):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(caminho_destino, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%")

# Exportar Google Docs
def exportar_google_file(service, file_id, mime_type_export, caminho_destino):
    request = service.files().export_media(fileId=file_id, mimeType=mime_type_export)
    fh = io.FileIO(caminho_destino, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Exportando {int(status.progress() * 100)}%")


def baixar_inteligente(service, file):
    file_id = file["id"]
    nome = file["name"]
    tipo = file["mimeType"]

    google_map = {
        "application/vnd.google-apps.document": ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".docx"),
        "application/vnd.google-apps.spreadsheet": ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx"),
        "application/vnd.google-apps.presentation": ("application/vnd.openxmlformats-officedocument.presentationml.presentation", ".pptx"),
        "application/vnd.google-apps.form": ("application/zip", ".zip"),
    }

    if tipo in google_map:
        export_mime, ext = google_map[tipo]
        return "export", export_mime, ext

    return "download", None, None

def baixar_recursivo(service, folder_id, pasta_local):
    os.makedirs(pasta_local, exist_ok=True)
    page_token = None

    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents",
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token
        ).execute()

        for f in response.get("files", []):
            file_id = f["id"]
            nome = alterar_caractere(f["name"])
            tipo = f["mimeType"]

            caminho = os.path.join(pasta_local, nome)

            if tipo == "application/vnd.google-apps.folder":
                print(f"\nCriando pasta: {caminho}")
                baixar_recursivo(service, file_id, caminho)
                continue

            print(f"\nProcessando: {nome}")

            acao, export_mime, ext = baixar_inteligente(service, f)

            if acao == "download":
                print(f"Baixando arquivo binário: {caminho}")
                baixar_arquivo(service, file_id, caminho)

            elif acao == "export":
                caminho_exportado = caminho + ext
                print(f"Exportando arquivo Google → {caminho_exportado}")
                exportar_google_file(service, file_id, export_mime, caminho_exportado)

        page_token = response.get("nextPageToken")
        if not page_token:
            break

def alterar_caractere(nome):
    caracteres_invalidos = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for c in caracteres_invalidos:
        nome = nome.replace(c, "_")
    return nome

def verificar_armazenamento(service):
    # Retorna o armazenamento total, usado e livre do Google Drive.

    info = service.about().get(fields="storageQuota").execute()
    quota = info["storageQuota"]

    total = int(quota["limit"])
    usado = int(quota["usage"])
    livre = total - usado

    porcentagem_usada = (usado / total) * 100

    gb = 1024 ** 3
    total_gb = total / gb
    usado_gb = usado / gb
    livre_gb = livre / gb

    print("\n=== ARMAZENAMENTO DO GOOGLE DRIVE ===")
    print(f"Total : {total_gb:.2f} GB")
    print(f"Usado : {usado_gb:.2f} GB ({porcentagem_usada:.2f}%)")
    print(f"Livre : {livre_gb:.2f} GB")

    return porcentagem_usada


def loop_continuo(limite_def=95, intervalo=60):
    while True:
        service_local = autenticar()

        print("\n[Verificando armazenamento...]")
        pct = verificar_armazenamento(service_local)

        if pct >= limite_def:
            pref_backup(service_local, origem="automatico", dias_para_backup=7)

        time.sleep(intervalo)



def ultimo_backup(dias_para_backup=7, diretorio="."):

    backups = [
        nome for nome in os.listdir(diretorio)
        if nome.startswith("backup-") and os.path.isdir(os.path.join(diretorio, nome))
    ]

    hoje = datetime.now().date()

    if not backups:
        return f"{diretorio}/backup-{hoje}"

    backups.sort(reverse=True)
    ultimo_backup = backups[0]

    data_str = ultimo_backup.replace("backup-", "")
    data_backup = datetime.strptime(data_str, "%Y-%m-%d").date()

    dias_passados = (hoje - data_backup).days

    if dias_passados >= dias_para_backup:
        return f"{diretorio}/backup-{hoje}"

    return None

def espaco_disponivel(caminho="."):
    total, usado, livre = shutil.disk_usage(caminho)
    return livre

def pref_backup(service, caminho_backup=None, origem="automatico", sobrescrever=False, dias_para_backup=7, diretorio="."):

    livre_local = espaco_disponivel(diretorio)  # diretório onde o backup será salvo
    info = service.about().get(fields="storageQuota").execute()
    quota = info["storageQuota"]
    usado_drive = int(quota["usage"])

    if livre_local < usado_drive:
        print(f"[{origem}] Espaço insuficiente para backup. Livre: {livre_local/(1024**3):.2f} GB, Necessário: {usado_drive/(1024**3):.2f} GB")
        for chat_id in CHATS_ID_TELEGRAM:
            try:
                bot.send_message(chat_id, "Espaço insuficiente para iniciar o backup automático. Verifique o armazenamento local!")
            except Exception as e:
                print(f"Falha ao enviar notificação para chat {chat_id}: {e}")
        return False

    if not backup_lock.acquire(blocking=False):
        print(f"[{origem}] Backup já em execução. Ignorando.")
        return False

    try:
        # Determinar caminho do backup
        if origem == "automatico":
            if not caminho_backup:
                caminho_backup = ultimo_backup(dias_para_backup=dias_para_backup, diretorio=diretorio)
            if not caminho_backup:
                print("[automatico] Backup recente já existe. Pulando.")
                return False

            for chat_id in CHATS_ID_TELEGRAM:
                try:
                    bot.send_message(chat_id, "Iniciando backup automático!")
                except Exception as e:
                    print(f"Falha ao enviar notificação para chat {chat_id}: {e}")

        elif origem == "telegram":
            if not caminho_backup:
                hoje = datetime.now().date()
                caminho_backup = f"{diretorio}/backup-{hoje}"

            if os.path.exists(caminho_backup) and not sobrescrever:
                print("[telegram] Backup já existe e não sobrescrever. Pulando.")
                return False

        print(f"[{origem}] Iniciando backup em {caminho_backup}...")
        baixar_recursivo(service, "root", caminho_backup)
        print(f"[{origem}] Backup finalizado com sucesso.")
        return True

    finally:
        backup_lock.release()

@bot.message_handler(commands=['start'])
def start(message):
    CHATS_ID_TELEGRAM.add(message.chat.id)
    bot.reply_to(
        message,
        "Bot de Backup Google Drive\n\n"
        "Comandos disponíveis:\n"
        "/backup_manual - Executar backup manual\n"
        "/armazenamento - Ver uso do Drive\n"
        "/status - Ver status do sistema"
    )

@bot.message_handler(commands=['backup_manual'])
def backup_manual(message):
    bot.reply_to(message, "Iniciando backup manual...")

    def tarefa():
        service_local = autenticar()
        sucesso = pref_backup(service_local, origem="telegram", sobrescrever=False)
        if sucesso:
            bot.send_message(message.chat.id, "Backup manual concluído com sucesso!")
        else:
            bot.send_message(
                message.chat.id,
                "Backup do dia já existe.\nUse /forcar_backup para sobrescrever."
            )

    threading.Thread(target=tarefa, daemon=True).start()



@bot.message_handler(commands=['armazenamento'])
def armazenamento(message):
    service_local = autenticar()
    info = service_local.about().get(fields="storageQuota").execute()
    quota = info["storageQuota"]

    total = int(quota["limit"])
    usado = int(quota["usage"])
    livre = total - usado

    pct_usado = (usado / total) * 100  # porcentagem usada
    gb = 1024 ** 3

    texto = (
        "*Armazenamento Google Drive*\n\n"
        f"Total : {total / gb:.2f} GB\n"
        f"Usado : {usado / gb:.2f} GB ({pct_usado:.2f}%)\n"
        f"Livre : {livre / gb:.2f} GB"
    )

    bot.send_message(message.chat.id, texto, parse_mode="Markdown")


@bot.message_handler(commands=['forcar_backup'])
def backup_forcado(message):
    bot.reply_to(message, "Iniciando backup manual FORÇADO...")

    def tarefa():
        service_local = autenticar()
        sucesso = pref_backup(service_local, origem="telegram", sobrescrever=True)

        if sucesso:
            bot.send_message(message.chat.id, "✅ Backup manual FORÇADO concluído com sucesso!")
        else:
            bot.send_message(
                message.chat.id,
                "⚠️ Backup já está em execução. Aguarde terminar para tentar novamente."
            )

    threading.Thread(target=tarefa, daemon=True).start()

@bot.message_handler(commands=['status'])
def status(message):
    em_execucao = backup_lock.locked()

    bot.reply_to(
        message,
        f"Status do sistema:\n"
        f"Backup em execução: {'SIM' if em_execucao else 'NÃO'}"
    )


if __name__ == "__main__":
    def iniciar_bot():
        print("Bot iniciado.")
        bot.infinity_polling()

    threading.Thread(target=iniciar_bot, daemon=True).start()
    loop_continuo(limite_def=70, intervalo=30)

