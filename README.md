# Proj.-intergrador-IFRN

# Bot de Backup Automático do Google Drive via Telegram

## 📌 Descrição do Projeto
Este projeto foi desenvolvido como parte da disciplina de **Projeto Integrador**. Trata-se de uma solução automatizada em Python que monitora o armazenamento do Google Drive e realiza backups preventivos para um servidor local, utilizando uma interface de controle via **Telegram Bot**..

O sistema permite:
- Realizar **backup automático** do Google Drive quando o armazenamento atinge um limite definido
- Executar **backup manual** via comandos no Telegram
- Exportar arquivos do Google Docs, Sheets e Slides para formatos compatíveis
- Monitorar o **uso de armazenamento** do Google Drive
- Garantir que não ocorram backups simultâneos

---

## 🎯 Objetivos
- Automatizar o processo de backup de arquivos na nuvem
- Evitar perda de dados por falta de espaço no Google Drive
- Permitir controle remoto via Telegram
- Aplicar conceitos de integração entre APIs, automação e concorrência

---

## 🧠 Funcionamento Geral
1. O sistema autentica o usuário no Google Drive usando OAuth 2.0
2. Monitora periodicamente o uso de armazenamento
3. Quando o limite configurado é atingido, inicia um backup automático
4. O usuário pode interagir com o sistema via **Telegram Bot**
5. Os arquivos são baixados de forma recursiva, preservando a estrutura de pastas
6. Arquivos do Google Docs são exportados para formatos compatíveis (.docx, .xlsx, .pptx)

---

## 🤖 Comandos do Bot Telegram
- `/start` → Inicia o bot e mostra os comandos disponíveis
- `/backup_manual` → Executa um backup manual
- `/forcar_backup` → Força a execução de um backup, mesmo que já exista
- `/armazenamento` → Mostra o uso do Google Drive
- `/status` → Verifica se há backup em execução

---

## 🛠 Tecnologias Utilizadas
- **Python 3**
- **Telegram Bot API**
- **Google Drive API**
- Bibliotecas:
  - `telebot`
  - `google-api-python-client`
  - `google-auth`
  - `threading`
  - `os`, `shutil`, `datetime`

---

## 📂 Estrutura do Projeto
