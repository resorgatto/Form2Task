# Form2Task

Automated integration of Typeform responses into ClickUp tasks

## Overview

This project automates the import of responses from Typeform forms into specific lists in ClickUp. The process can be executed manually or scheduled to run periodically, making it easy to keep your ClickUp tasks updated with new responses.

## Features

- Fetches responses from one or more Typeform forms
- Automatically creates tasks in ClickUp lists
- Tracks processing status via a local storage file
- Supports manual or automated execution (cron, Windows Task Scheduler, or systemd timer)

## Requirements

- Python 3.8 or higher
- Valid API tokens for Typeform and ClickUp
- Windows, Linux, or any compatible operating system

## Installation

1. **Download or clone the project:**

   git clone <repository-url>
   cd Form2Task

    Create a Python virtual environment:

python3 -m venv venv
## Or on Windows:
 python -m venv venv

Activate the virtual environment:

    Linux/macOS:

source venv/bin/activate

Windows:

    venv\Scripts\activate

Install dependencies:

    pip install -r requirements.txt

    Set the required environment variables:

        COPIER_TYPEFORM_AUTH_TOKEN

        COPIER_TYPEFORM_WORKSPACE_ID

        COPIER_CLICKUP_LIST

        COPIER_CLICKUP_AUTH_TOKEN

Usage

Run the script manually:

python script.py --migrate

Make sure all environment variables are set before running the script.
Setting environment variables

    Linux/macOS:

    export COPIER_TYPEFORM_AUTH_TOKEN=SEU_TOKEN_TYPEFORM
    export COPIER_TYPEFORM_WORKSPACE_ID=SEU_WORKSPACE_ID
    export COPIER_CLICKUP_LIST=ID_DA_SUA_LISTA
    export COPIER_CLICKUP_AUTH_TOKEN=SEU_TOKEN_CLICKUP

Windows (cmd):

    set COPIER_TYPEFORM_AUTH_TOKEN=YOUR_TYPEFORM_TOKEN
    set COPIER_TYPEFORM_WORKSPACE_ID=YOUR_WORKSPACE_ID
    set COPIER_CLICKUP_LIST=YOUR_CLICKUP_LIST_ID
    set COPIER_CLICKUP_AUTH_TOKEN=YOUR_CLICKUP_TOKEN

Automation

    Windows:
    Use Windows Task Scheduler to run the script at the desired interval.

    Linux:
    Use cron or a systemd timer to schedule script execution.

Storage

The script uses a local armazenamento.json file in the project directory to track processed responses.
License

This project is provided as-is, with no guarantee of suitability for any particular environment.

Questions?
Open an issue in the repository.


---

Let me know if you want a more concise version, or if you’d like to include example schedul



#### pt-br

# Form2Task

Automação de integração entre respostas do Typeform e tarefas no ClickUp

## Visão Geral

Este projeto automatiza a importação de respostas de formulários Typeform para tarefas em listas do ClickUp. O processo pode ser executado manualmente ou agendado para rodar periodicamente, facilitando o processamento contínuo de novas respostas.

## Funcionalidades

- Busca respostas em formulários do Typeform
- Cria tarefas automaticamente em listas do ClickUp
- Controle de estado do processamento via arquivo local
- Execução manual ou automatizada (cron, agendador de tarefas ou systemd timer)

## Pré-requisitos

- Python 3.8 ou superior
- Conta e tokens de API válidos do Typeform e ClickUp
- Sistema operacional Windows, Linux ou compatível

## Instalação

1. **Baixe ou clone o projeto:**
   ```bash
   git clone <url-do-repositorio>
   cd Form2Task

    Crie o ambiente virtual Python:

python3 -m venv venv
## Ou no Windows:
 python -m venv venv

Ative o ambiente virtual:

    Linux/macOS:

source venv/bin/activate

Windows:

    venv\Scripts\activate

Instale as dependências:

    pip install -r requirements.txt

    Defina as variáveis de ambiente necessárias:

        COPIER_TYPEFORM_AUTH_TOKEN

        COPIER_TYPEFORM_WORKSPACE_ID

        COPIER_CLICKUP_LIST

        COPIER_CLICKUP_AUTH_TOKEN

Uso

Execute manualmente o script, por exemplo:

python script.py --migrate

Certifique-se de que as variáveis de ambiente estão definidas antes de executar.
Definindo variáveis de ambiente

    Linux/macOS:

    export COPIER_TYPEFORM_AUTH_TOKEN=SEU_TOKEN_TYPEFORM
    export COPIER_TYPEFORM_WORKSPACE_ID=SEU_WORKSPACE_ID
    export COPIER_CLICKUP_LIST=ID_DA_SUA_LISTA
    export COPIER_CLICKUP_AUTH_TOKEN=SEU_TOKEN_CLICKUP

Windows (cmd):

    set COPIER_TYPEFORM_AUTH_TOKEN=SEU_TOKEN_TYPEFORM
    set COPIER_TYPEFORM_WORKSPACE_ID=SEU_WORKSPACE_ID
    set COPIER_CLICKUP_LIST=ID_DA_SUA_LISTA
    set COPIER_CLICKUP_AUTH_TOKEN=SEU_TOKEN_CLICKUP

Execução automática

    Windows:
    Use o Agendador de Tarefas do Windows para rodar o script periodicamente.

    Linux:
    Use cron ou systemd timer para agendar a execução do script.

Armazenamento

O script utiliza um arquivo armazenamento.json no diretório do projeto para controle de estado.
Licença

Este projeto é fornecido como está, sem garantia de funcionamento em todos os ambientes.

Dúvidas?
Abra uma issue no repositório.
