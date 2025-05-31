import requests
import mimetypes
import os
import tempfile
import shutil
import subprocess
import sys

# Downloads and pushes a file from a remote URL
# Returns clickup attachment URL
def push_attachment(source_url: str, task: int, source_headers=None, headers=None) -> str:
    # NOTE the stream=True parameter below

    tmp = tempfile.NamedTemporaryFile(delete=False)
    
    # Abra o arquivo temporário uma única vez antes do loop
    with open(tmp.name, "wb") as f: # <-- Movido para fora do loop
        with requests.get(source_url, stream=True, headers=source_headers) as r:
            r.raise_for_status()

            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # É uma boa prática verificar se o chunk não está vazio
                    # print(f"writing chunk of size {len(chunk)} bytes")
                    f.write(chunk)
    

    with open(tmp.name, "rb") as a:
        mime_type, encoding = mimetypes.guess_type(tmp.name) 
        name = os.path.basename(tmp.name)
        name = source_url.split("/")[-1]
        url = f"https://api.clickup.com/api/v2/task/{task}/attachment"
 
        response = requests.post(url, headers=headers, files={"attachment": (name, a, mime_type)})
        return response.json()["url"]