# deployment/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend /app/backend
COPY ./frontend /app/frontend

WORKDIR /app/backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# deployment/docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app/backend
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydatabase
      - OPENAI_API_KEY=${OPENAI_API_KEY}
  
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydatabase
    ports:
      - "5432:5432"

# deployment/requirements.txt
fastapi
uvicorn
psycopg2-binary
langchain
openai

# deployment/.env
OPENAI_API_KEY=your_openai_api_key

# deployment/ci-cd.yml
version: 2.1

jobs:
  build:
    docker:
      - image: docker:19.03.12
    steps:
      - setup_remote_docker:
          version: 20.10.7
          docker_layer_caching: true
      - run:
          name: Build Docker Image
          command: docker build -t myapp:latest .
      - run:
          name: Run Tests
          command: docker run myapp:latest pytest

  deploy:
    docker:
      - image: docker:19.03.12
    steps:
      - run:
          name: Deploy to Cloud
          command: |
            echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
            docker push myapp:latest

workflows:
  version: 2
  build_and_deploy:
    jobs:
      - build
      - deploy:
          requires:
            - build