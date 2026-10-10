FROM python:3.11-alpine
WORKDIR /app
COPY seed.py .
ENTRYPOINT ["python", "seed.py"]
CMD ["--api-url", "http://api:8000/api/v1"]
