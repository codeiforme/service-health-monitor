FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY app/ ./app/
USER 10001:10001
CMD ["python", "-m", "app.monitor"]
