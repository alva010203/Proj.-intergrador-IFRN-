# Proj.-intergrador-IFRN
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Google Drive API](https://img.shields.io/badge/API-Google%20Drive%20v3-green.svg)](https://developers.google.com/drive)
[![Telegram Bot API](https://img.shields.io/badge/Bot-Telegram%20API-blue.svg)](https://core.telegram.org/bots)

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

## 🤖 Interface do Bot (Comandos)

| Comando | Descrição |
| :--- | :--- |
| `/start` | Inicializa o bot e apresenta o menu de ajuda. |
| `/armazenamento` | Exibe relatório de cota (Total, Usado, Livre) com barra de porcentagem. |
| `/backup_manual` | Inicia o download se não houver backup recente. |
| `/forcar_backup` | Sobrescreve backups existentes e inicia nova sincronia. |
| `/status` | Verifica se o sistema está ocioso ou processando arquivos. |

---

## 🛠 Tecnologias Utilizadas
- **Python 3.x**
- **[Telegram Bot API](https://core.telegram.org/bots)**
- **[Google Drive API v3](https://developers.google.com/drive/api)**
- Bibliotecas:
  - `telebot`
  - `google-api-python-client`
  - `google-auth`
  - `threading`
  - `os`, `shutil`, `datetime`

---

## 📂 Estrutura do Projeto

---

## ⚙️ Configuração e Instalação

### 1. Requisitos Prévios
* Conta no [Google Cloud Console](https://console.cloud.google.com/). (corrigir se necessário)
* Ativar a **Google Drive API**.
* Download do arquivo `credentials.json` (OAuth 2.0).
*  

### 2. Dependências
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib pyTelegramBotAPI
