FROM python:3.11-alpine
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 3500
CMD ["python","app.py"]
