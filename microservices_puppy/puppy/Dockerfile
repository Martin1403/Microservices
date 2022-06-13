FROM python:3.7-slim
RUN mkdir "puppy"
COPY requirements.txt puppy/requirements.txt
RUN pip install -U pip
RUN pip install -r puppy/requirements.txt
COPY . /puppy
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001
ENV FLASK_ENV=development
ENV FLASK_APP=puppy
EXPOSE 5001
ENTRYPOINT ["flask"]
CMD ["run"]
