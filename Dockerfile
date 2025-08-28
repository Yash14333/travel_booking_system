FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY . /code/
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc build-essential --no-install-recommends && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput || true
EXPOSE 8000
CMD ["gunicorn", "travel_booking.wsgi:application", "--bind", "0.0.0.0:8000"]
