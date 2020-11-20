FROM python:3.8-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT 8080
ENV PYTHONUNBUFFERED TRUE

CMD python ./manage.py runserver 0.0.0.0:$PORT