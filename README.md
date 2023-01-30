# Focos Queimadas - API 

## 1. Objetivo 
    
Busca-se construir uma API que seja capaz de disponibilizar os dados referentes a focos de calor no Brasil nas últimas 24 ou 48 horas.

## 2. Solução 

Conforme os arquivos .json disponibilizados pelo INPE, um dos módulos baixa o arquivo (24h ou 48h) e a API consome as informações desse arquivo conforme os dados de entrada. \
Nesta aplicação, os dados de entrada são os códigos de município e estado do IBGE. Dessa forma, são retornados os dados referentes aos focos de queimadas nos municípios brasileiros nas últimas 24 ou 48 horas. \
Por opção, foi escolhido apenas trabalhar com os dados do Brasil e não da América do Sul como um todo ou com informações dos estados individualmente.

Os dados são obtidos a partir do seguinte endereço:
* https://queimadas.dgi.inpe.br/queimadas/dados-abertos/ 

### 2.1 Primeiros Passos

``` shell
pip install -r requirements.txt
```

## 3. Implementação

## 4. Descrição 

## 5. Conteúdo

## 6. Resultados

```
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