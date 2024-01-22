FROM python:3.10

WORKDIR /home/myproj

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -v

COPY . .
