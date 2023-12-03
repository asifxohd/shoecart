FROM python:3.10

ENV PYTHONUNBUFFERED=1
RUN apt-get update -q && apt-get install -yq libpq-dev && apt-get install -y postgresql-client

WORKDIR /app 

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run the migration command
RUN python manage.py migrate

# Import data from dump_file.sql
RUN psql -U postgres -d postgres_container -f dump_file.sql
