FROM python:3.9-slim

# App name
ARG APP="stt"

RUN mkdir $APP
COPY requirements.txt $APP/requirements.txt
RUN pip install -U pip
RUN pip install -r $APP/requirements.txt
COPY . /$APP

# If you want to have scorer (990Mb):
RUN apt-get update && apt-get -y install wget
RUN wget -O $APP/model/output_graph.scorer https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

# Settings:
ENV QUART_APP=$APP.app:app
ENV QUART_ENV=development
EXPOSE 5001

CMD quart run -h "0.0.0.0" -p 5001