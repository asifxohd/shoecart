FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
ENV NAME World
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
