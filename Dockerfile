FROM ubuntu:latest
FROM python:3.11.1-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]