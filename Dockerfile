# dockerfile, image, container
# blueprint for building images, template for containers, running process with app 

FROM python:3.10

WORKDIR /code

COPY ./requirements-loose.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt 

COPY . /code/

CMD ["python", "/code/main_discord_bot.py"]

# Notes

# building the app: 
# docker build -t image-name .

# running the app: 
# docker run container-name | image-name

# run interactive with user-input
# docker run -i -t container-name | image-name

# running in the background
# docker run -d --name container-name -p 80:80 image-name

# running webapp
# CMD ["runcmd", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# start existing container
# docker start container-name

# get terminal into running container
# docker exec -it <container-id> /bin/sh
