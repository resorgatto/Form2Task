from typing import Final
import json
import requests
from dataclasses import dataclass
from loguru import logger
from enum import Enum
import enum
import re


class FieldType(Enum):
    multiple_choice = "multiple_choice"
    short_text = "short_text"
    text = "text"
    file_upload = "file_upload"
    number = "number"
    phone_number = "phone_number"
    date = "date"
    email = "email"

def to_entrytype(fieldtype: FieldType) -> FieldType:
    match fieldtype:
        case FieldType.short_text:
            return "text"
        case FieldType.file_upload:
            return "file_url"
        case FieldType.multiple_choice:
            return "choice"
        case _:
            return fieldtype.name 

@dataclass
class Field:
    name: str
    field_type: FieldType

type FormFields = dict["ref": Field]
type Answer = dict[Field] 

@dataclass
class UserAnswer:
    id: str
    date: str
    answers: list[Answer]

@dataclass
class Form:
    id: str
    title: str
    fields: FormFields


TYPEFORM_API_ENDPOINT = "https://api.typeform.com"

date_format = "%Y-%m-%dT%H:%M:%SZ"

field_template_pattern = r"\{\{.*?\}\}" # {{field:blablabla}}
clean_text = lambda x: re.sub(field_template_pattern, "", x).removeprefix(", ")



def get_refs(session: requests.Session, form_id: str, endpoint: str = "https://api.typeform.com", headers=None) -> Form:
    response = session.get(f"{endpoint}/forms/{form_id}", headers=headers).json()
    fields_from_form: FormFields = {}
    for field in response["fields"]:
        fields_from_form[field["ref"]] = Field(name=clean_text(field["title"]), field_type=[field["type"]])
    return Form(fields=fields_from_form, id=form_id, title=response["title"])



def get_responses(session: requests.Session, form: str, fields: FormFields, endpoint: str = "https://api.typeform.com", headers=None) -> list[UserAnswer]:
    get_forms = session.get(f"{endpoint}/forms/{form}/responses", headers=headers)

    users_answers: list[UserAnswer] = []
    for item in get_forms.json()["items"]:
        # Contexto que provem todas as respostas de um usuario
        user_answer = {}
        for answer in item["answers"]:
            fieldattr = answer["field"]
            fieldtype: FieldType = fields[fieldattr['ref']]
            field_title: str = fieldtype.name
            try:
                user_value = answer[to_entrytype(FieldType[str(fieldtype.field_type[0]).lower()])] 
            except:
                print(f"Falha ao ler novo elemento do bglh, adiciona no Enum: {field_title}: {fieldtype.field_type[0]}")
            user_answer[clean_text(field_title)] = Field(field_type=fieldtype.field_type, name=user_value)
        users_answers.append(UserAnswer(answers=user_answer, date=item["landed_at"], id=item["landing_id"]))
    return users_answers 