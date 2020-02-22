FROM python:3.8
WORKDIR /app

COPY ./Pipfile* .
RUN pipenv install

COPY . .

CMD ["pipenv", "run", "python", "run.py"]
