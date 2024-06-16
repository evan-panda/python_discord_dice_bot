FROM python:3.12

WORKDIR /code

COPY ./requirements-loose.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt 

# CMD ["python", "main_discord_bot.py"]
