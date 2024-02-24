FROM python:3.10

WORKDIR /code

COPY ./requirements-loose.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt 

CMD ["python", "main_discord_bot.py"]

