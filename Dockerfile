FROM python:3.12-slim
WORKDIR /app
COPY analyse.py .
ENTRYPOINT ["python", "analyse.py"]
