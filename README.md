# Focos Queimadas - API 

## 1. Objetivo

Busca-se construir uma API que seja capaz de disponibilizar os dados referentes a focos de calor no Brasil nas últimas 24 ou 48 horas.

## 2. Solução 

Conforme os arquivos .json disponibilizados pelo INPE, um dos módulos baixa o arquivo (24h ou 48h) e a API consome as informações desse arquivo conforme os dados de entrada. \
\
Nesta aplicação, os dados de entrada são os códigos de município e estado do IBGE. Dessa forma, são retornados os dados referentes aos focos de queimadas nos municípios brasileiros nas últimas 24 ou 48 horas. \
\
Por opção, foi escolhido apenas trabalhar com os dados do Brasil e não da América do Sul como um todo ou com informações dos estados individualmente. \
\
Os dados são obtidos a partir do seguinte endereço:
* https://queimadas.dgi.inpe.br/queimadas/dados-abertos/ 

### 2.1 Primeiros Passos

1. Clone este repositório:  `git@github.com:guimaraesf/api-focos-queimadas.git` 
2. Inicie seu ambiente virtual: `virtualenv api-focos-queimadas`
3. Instale os requisitos com:  `pip install -r requirements.txt`
4. Curl: `curl -X 'GET' 'http://127.0.0.1:8001/focos' -H 'accept: application/json'`
5. Request URL: `http://127.0.0.1:8001/focos`

## 3. Implementação

Conforme a arquitetura proposta, a abaixo segue a ilustração do processo.

![desenho](imgs/api.png)

## 4. Descrição

Os dados que alimentam a API são extraídos do portal de dados abertos do INPE, onde são publicados diariamente as informações referentes aos focos de calor na América do Sul, Brasil ou Unidades Federativas. \
\
São disponibilizados dados nos formatos csv ou json. Por opção, foi escolhido capturar esses dados em formato json. Para tal, foi desenvolvido um script python que realiza o scraping desses dados. \
\
Com os dados capturados e salvos em um diretório local, a API então faz uso dos dados, sejam eles das últimas 24 ou 48 horas.

### 4.1 Endpoints

### GET 

```/api/health```: Verifica a integridade das requisições 

### Código HTTP

201 (CREATED)

### Resposta

```json
{
  "status": "Healthy",
  "totalTimeTaken": "0:00:00",
  "entities": []
}
```
\
```/focos```: Retorno dos dados de focos de calor nas últimas 24 ou 48 horas

### Código HTTP

200 (OK)


### Parâmetros

|           Name | Required |    Type    | Description                 |
|---------------:|:--------:|:----------:|-----------------------------|
| `municipio_id` | opcional |  integer   | Código do município do IBGE |
|    `estado_id` | opcional |  integer   | Código do município do IBGE |


### Resposta

```json
[
  {
    "id": "51f9a15f-4f00-30ec-8694-a38e791f4f32",
    "longitude": -61.72956,
    "latitude": 2.6239,
    "data_hora_gmt": "2023-01-26T17:56:00+00:00",
    "satelite": "AQUA_M-T",
    "municipio": "MUCAJAÍ",
    "estado": "RORAIMA",
    "pais": "Brasil",
    "municipio_id": 1400308,
    "estado_id": 14,
    "pais_id": 33,
    "numero_dias_sem_chuva": 5,
    "precipitacao": 0,
    "risco_fogo": 0.06,
    "bioma": "Amazônia"
  }
]
```
\
```/focos/atributos/municipios```: Retorno dos dados de observações únicas de municípios.

### Código HTTP
200 (OK)


### Resposta

```json
[
  {
    "pais_id": 33,
    "pais": "Brasil",
    "estado_id": 14,
    "estado": "RORAIMA",
    "municipio_id": 1400308,
    "municipio": "MUCAJAÍ"
  }
]
```
\
```/focos/atributos/estados```: Retorno dos dados de observações únicas de estados.

### Código HTTP
200 (OK)


### Resposta

```json
[
  {
    "pais_id": 33,
    "pais": "Brasil",
    "estado_id": 14,
    "estado": "RORAIMA"
  }
]
```
\
```/focos/atributos/biomas```: Retorno dos dados de observações únicas de biomas.

### Código HTTP
200 (OK)

### Resposta

```json
[
  {
    "bioma": "Amazônia"
  }
]
```
\
```/focos/atributos/satelites```: Retorno dos dados de observações únicas de satelites.

### Código HTTP

200 (OK) 

### Resposta

```json
[
  {
    "satelite": "AQUA_M-T"
  }
]
```

## 5. Conteúdo
Nesta seção é descrito o que cada módulo da aplicação executa. 

* **main.py**: Script python principal responsável pelo desenvolimento da API.
* **models.py:** Script python que contém os schemas utilizados nos endpoints.
* **utils.py**: Script python que contém os principais métodos que são utilizados no arquivo main. 
* **download_file.py**: Script python responsável por realizar o download do arquivo no portal de dados abertos. 
* **Dockerfile**: Script Docker para construir o contâiner da aplicação.
* **requirements.txt**: Arquivo com os requisitos usados no ambiente.


