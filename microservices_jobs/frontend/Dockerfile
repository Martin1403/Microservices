FROM python:3.9-slim

ARG APP="frontend"

RUN mkdir $APP
COPY requirements.txt $APP/requirements.txt
RUN pip install -U pip
RUN pip install -r $APP/requirements.txt
COPY . /$APP

ENV DOCKER=1
ENV FLASK_ENV=development
ENV FLASK_APP=$APP

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
EXPOSE 5001

ENTRYPOINT ["flask"]
CMD ["run"]
