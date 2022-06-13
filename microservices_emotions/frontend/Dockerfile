FROM python:3.9-slim

RUN mkdir frontend
RUN pip install -U pip
COPY requirements.txt frontend/requirements.txt
RUN pip install -r frontend/requirements.txt

COPY . frontend/

# Settings:
ENV DOCKER=1
ENV DEBUG=0
ENV HOST=0.0.0.0
ENV PORT=5000
EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["frontend"]