FROM python:3.7-slim
RUN mkdir "frontend"
COPY requirements.txt frontend/requirements.txt
RUN pip install -U pip
RUN pip install -r frontend/requirements.txt
COPY . /frontend
ENV DOCKER=1
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_ENV=development
ENV FLASK_APP=frontend
EXPOSE 5000
ENTRYPOINT ["flask"]
CMD ["run"]
