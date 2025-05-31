FROM cgr.dev/chainguard/python:latest-dev

COPY . /app 
WORKDIR /app

USER 0

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "/app/script.py"]