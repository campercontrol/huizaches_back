# Pull base image
FROM python:3.9-slim-buster

WORKDIR /app
COPY ./app /app

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r ./requirements.txt

RUN apt-get update 
RUN apt install 

EXPOSE 8000

#CMD ["uvicorn", "main:app" ,"--host", "0.0.0.0", "--port", "8080", "--reload"]


