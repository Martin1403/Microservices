FROM python:3.9-slim

ARG APP="users"

RUN mkdir $APP
COPY requirements.txt $APP/requirements.txt
RUN pip install -U pip
RUN pip install -r $APP/requirements.txt
COPY . /$APP

ENV FLASK_ENV=development
ENV FLASK_APP=$APP

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5002
EXPOSE 5002

ENTRYPOINT ["flask"]
CMD ["run"]
