FROM python:3.9-slim

RUN mkdir emotions
RUN pip install -U pip
COPY requirements.txt emotions/requirements.txt
RUN pip install -r emotions/requirements.txt

COPY . emotions/

# Settings:
ENV DEBUG=0
ENV HOST=0.0.0.0
ENV PORT=5002
EXPOSE 5002

ENTRYPOINT ["python"]
CMD ["emotions"]