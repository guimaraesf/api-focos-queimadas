FROM python:3.9

WORKDIR /C:/Development/portfolio/api/

COPY ./requirements.txt /C:/Development/portfolio/api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /C:/Development/portfolio/api/requirements.txt

COPY ./app /C:/Development/portfolio/api/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "log_level", "info"]