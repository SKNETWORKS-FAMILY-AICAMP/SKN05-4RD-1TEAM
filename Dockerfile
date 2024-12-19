# pull official base image
FROM python:3.10.14

# set work directory
WORKDIR /usr/src/app

# Update package list and install dependencies
RUN apt-get update && apt-get install -y \
    postgresql libpq-dev gcc python3-dev zlib1g-dev libjpeg-dev

COPY . /usr/src/app/



RUN pip install --upgrade pip


RUN pip install -r requirements.txt


CMD ["/bin/bash", "-c", "0.0.0.0:8000", "tail -f /dev/null" ]
