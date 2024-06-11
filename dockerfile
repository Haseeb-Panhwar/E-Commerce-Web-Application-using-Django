FROM python:3.11-bullseye

ENV PYTHONBUFFERED=1

WORKDIR /django

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD gunicorn ecommercesite.wsgi:application --bind 0.0.0.0:8001

EXPOSE 8001