FROM python:3.8
WORKDIR /portal
EXPOSE 80 443 5000
RUN apt update && apt install python3-venv -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD python __init__.py