FROM python:3.8
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir pipenv

COPY ./Pipfile* ./
RUN pipenv install

COPY . .

CMD ["pipenv", "run", "python", "run.py"]
