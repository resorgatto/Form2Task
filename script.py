import typeform
from pathlib import Path
import requests
from datetime import datetime
from pprint import pprint
from loguru import logger
import clickup
import typer
import json
import sys
import os


typeform_auth_token = os.environ["COPIER_TYPEFORM_AUTH_TOKEN"]
typeform_workspace_id = os.environ["COPIER_TYPEFORM_WORKSPACE_ID"]
typeform_headers = {"Authorization": f"Bearer {typeform_auth_token}"}

HARCODED_LIST = os.environ["COPIER_CLICKUP_LIST"]
CLICKUP_API_ENDPOINT = "https://api.clickup.com/api/v2"
clickup_headers = {
    "accept": "application/json",
    "Authorization": os.environ["COPIER_CLICKUP_AUTH_TOKEN"]
}
 

def migrate_to_clickup(form_target: str, data_target: datetime) -> int:
    logger.debug("Inicializando")
    # [ field name = value ]
    responses: list[typeform.Answer] = [] 
    form: typeform.Form = None
    with requests.Session() as s:
        form = typeform.get_refs(s, form_target, headers=typeform_headers)
        responses: list[typeform.UserAnswer] = typeform.get_responses(s, form_target, form.fields, headers=typeform_headers)


    # comeca por 2022, termina por 2025
    # datas_formatadas = sorted(responses, key=lambda x: datetime.strptime(x.date, typeform.date_format))
    datas_apos_dia: list[typeform.UserAnswer] = list(filter(lambda x: datetime.strptime(x.date, typeform.date_format) > data_target, responses)) 

    # Cria a task
    task_do_usuario = {}
    with requests.Session() as s: 
        for task in datas_apos_dia:
            form = typeform.get_refs(s, form_target, headers=typeform_headers)
            post = s.post(f"{CLICKUP_API_ENDPOINT}/list/{HARCODED_LIST}/task", headers=clickup_headers, json={"name": form.title})
            print(post.json())
            task_do_usuario[post.json()["id"]] = task 

    with requests.Session() as s:
        for id_task, usuario in task_do_usuario.items(): 
            # Adiciona attachments e descricao para task
            string_enorme = "\n"
            for field, value in usuario.answers.items():
                if value.field_type[0] == "file_upload":
                    link_retorno = clickup.push_attachment(value.name, task=id_task, source_headers=typeform_headers, headers=clickup_headers)
                    string_enorme += f"### {field}\n- {link_retorno}\n\n" 
                    continue
                string_enorme += f"### {field}\n- {value.name}\n\n" 
            
            putando = s.put(f"{CLICKUP_API_ENDPOINT}/task/{id_task}", headers=clickup_headers, json={"name": form.title, "markdown_content": string_enorme})
            
            pprint(putando.json())



    return 0

def main(storage_file: str = "armazenamento.json", migrate: bool = False) -> int:
    logger.debug('Inicializacao funcionou')
    try:
        with open(storage_file, "r") as arq:
            datas = json.load(arq)
    except json.JSONDecodeError:
        logger.critical(f'Falha ao ler arquivo de armazenamento {storage_file} como JSON.')
        return 2
    except FileNotFoundError:
        logger.critical(f'Falha ao ler arquivo de armazenamento {storage_file}.')
        Path(storage_file).write_text("{}")
        return 2


    logger.debug("Verificando os formulários do workspace: {typeform_workspace_id}")
    with requests.Session() as s:
        logger.debug(f"Pegando formularios do workspace: {typeform_workspace_id}")
        forms = s.get(f"{typeform.TYPEFORM_API_ENDPOINT}/forms?workspace_id={typeform_workspace_id}", headers=typeform_headers)
        for form in forms.json()["items"]: 
            logger.debug(f"Pegando repostas do formulário: {form["id"]}")
            with s.get(f"{typeform.TYPEFORM_API_ENDPOINT}/forms/{form["id"]}/responses", headers=typeform_headers) as formulario_tal:
                data_inicial = ""
                logger.debug(f"")
                
                if form["id"] in datas:
                    data_inicial = datetime.strptime(datas[form["id"]], typeform.date_format)
                
                respostas_formatadas = list(sorted(formulario_tal.json()["items"], key=lambda x: datetime.strptime(x["landed_at"], typeform.date_format)))
                data_nova = respostas_formatadas[-1]["landed_at"]

                if migrate:
                    logger.info(f"Iniciando migracao do formulario \"{form['title']}\"")
                    try:
                        if form["id"] in datas:
                            migrate_to_clickup(form["id"], data_inicial)
                        else:
                            migrate_to_clickup(form["id"], data_nova)
                    except:
                        logger.debug("fodase")
                    logger.info(f"Migração concluida com sucesso!!")

                datas[form["id"]] = data_nova 

    logger.info(f"Escrevendo dados atualizado para {storage_file}")
    logger.debug(datas)
    with open(storage_file, "w") as arm:
        json.dump(datas, arm, indent=4)
    return 0


if __name__ == "__main__":
    typer.run(main)
    