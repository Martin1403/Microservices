FROM python:3.9-slim

# App name
ARG APP="app"

RUN mkdir $APP
COPY requirements.txt $APP/requirements.txt
RUN pip install -U pip
RUN pip install -r $APP/requirements.txt
COPY . /$APP

# Settings:
ENV QUART_APP=$APP.app:app
ENV QUART_ENV=development
EXPOSE 5001

CMD quart run -h "0.0.0.0" -p 5001