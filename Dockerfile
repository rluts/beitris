FROM python:3.8


WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

ADD . /app
#RUN python manage.py collectstatic --no-input

EXPOSE 8000
CMD ["gunicorn", "beitris.wsgi", "--bind", "0.0.0.0:8000"]
