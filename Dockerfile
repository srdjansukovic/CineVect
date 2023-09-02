FROM python:3.10-slim-buster

RUN apt-get update && \
  apt-get install -y git && \
  apt-get install -y git-lfs

WORKDIR /app

RUN git lfs install && git clone https://huggingface.co/sentence-transformers/all-mpnet-base-v2

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "-u", "main.py"]