FROM python:3.9-slim

RUN mkdir posts
RUN pip install -U pip
COPY requirements.txt posts/requirements.txt
RUN pip install -r posts/requirements.txt

COPY . posts/

# Settings:
ENV DOCKER=1
ENV DEBUG=0
ENV HOST=0.0.0.0
ENV PORT=5001
EXPOSE 5001

ENTRYPOINT ["python"]
CMD ["posts"]