FROM python:3.9

WORKDIR /C:/Development/repositorios/api-focos-queimadas

COPY ./requirements.txt /C:/Development/repositorios/api-focos-queimadas/requirements.txt

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade -r /C:/Development/portfolio/api/requirements.txt

COPY ./app /C:/Development/repositorios/api-focos-queimadas/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "log_level", "info"]