
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8050

CMD ["python", "src/server.py"]
