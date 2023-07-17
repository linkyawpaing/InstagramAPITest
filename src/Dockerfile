FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

COPY ./app .

# CMD ["python", "app.py"]
CMD ["uwsgi", "--ini", "app.ini"]