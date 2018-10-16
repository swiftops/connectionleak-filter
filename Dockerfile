FROM python:alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6003

CMD [ "gunicorn", "--config", "gunicorn_config.py", "services:app" ]