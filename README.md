# Projeto-intergrador-IFRN
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Google Drive API](https://img.shields.io/badge/API-Google%20Drive%20v3-green.svg)](https://developers.google.com/drive)
[![Telegram Bot API](https://img.shields.io/badge/Bot-Telegram%20API-blue.svg)](https://core.telegram.org/bots)

# Bot de Backup Automático do Google Drive via Telegram

## 📌 Descrição do Projeto
Este projeto foi desenvolvido como parte da disciplina de **Projeto Integrador (IFRN)**.  
A solução consiste em um **sistema automatizado em Python** capaz de monitorar o armazenamento do **Google Drive** e realizar **backups preventivos para um ambiente local**, utilizando uma interface de controle remoto via **Telegram Bot**.

O sistema permite:
- Realizar **backup automático** do Google Drive ao atingir um limite de uso configurado
- Executar **backup manual** por meio de comandos no Telegram
- Exportar arquivos do Google Docs, Sheets e Slides para formatos compatíveis
- Monitoramento continuo do **uso de armazenamento**
- Evitar a execução simultânea de múltiplos backups

---

## 🎯 Objetivos
- Automatizar o processo de backup de arquivos armazenados na nuvem
- Reduzir riscos de perda de dados por falta de espaço no Google Drive
- Permitir gerenciamento remoto do sistema por meio do Telegram
- Aplicar conceitos de **integração de APIs**, **automação** e **programação concorrente**

---

## 🧠 Funcionamento Geral
1. O sistema autentica o usuário no Google Drive utilizando OAuth 2.0
2. Monitora periodicamente o consumo de armazenamento
3. Ao atingir o limite configurado, inicia automaticamente o processo de backup
4. O usuário pode interagir com o sistema por meio de comandos no Telegram
5. Os arquivos são baixados de forma recursiva, mantendo a estrutura de pastas
6. Arquivos do Google Workspace são exportados para formatos compatíveis (.docx, .xlsx, .pptx)

---

## 🤖 Interface do Bot (Comandos)

| Comando | Descrição |
|------|----------|
| `/start` | Inicializa o bot e exibe os comandos disponíveis |
| `/armazenamento` | Exibe informações de uso do Google Drive |
| `/backup_manual` | Executa backup caso não exista um recente |
| `/forcar_backup` | Força a execução de um novo backup |
| `/status` | Verifica se há backup em execução |

---

## 🛠 Tecnologias Utilizadas
- **Python 3.x**
- **Telegram Bot API**
- **Google Drive API v3**
- Bibliotecas:
  - `pyTelegramBotAPI`
  - `google-api-python-client`
  - `google-auth`
  - `google-auth-oauthlib`
  - `threading`
  - `os`, `shutil`, `datetime`

---

## 📂 Estrutura do Projeto
```
Proj.-intergrador-IFRN/
├── main.py
├── credentials.json
├── token.json
├── backup-YYYY-MM-DD/
├── README.md
```

---

## ⚙️ Configuração e Instalação

### Tutorial Api drive
#### Entre nesse link para realizar o tutorial.
https://console.cloud.google.com/
#### Passo a Passo
https://drive.google.com/file/d/1d1oZH9m1T1OWoNh59p_ERDu6903NpOnd/view?usp=sharing

### 1️⃣ Requisitos Prévios
- Conta no **Google Cloud Console** (corrigir se necessário)
- Google Drive API ativada
- Arquivo `credentials.json` (OAuth 2.0)

### 2️⃣ Instalação das Dependências
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib telebot


