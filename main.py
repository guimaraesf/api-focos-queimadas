import os
import uvicorn
from typing import List, Optional
from utils.utils import (get_json_file, get_result_atribute, get_result_municipios,
                         get_result_estados, get_all_results, get_result_atribute_municipios)
from fastapi import (FastAPI, HTTPException, status, Query)
from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute
from models import (HealthCheckSchema, PropertiesSchema, MunicipiosSchema,
                    BiomasSchema, SatelitesSchema, Responses)


# inputs ------------------------------------------------------------------- #

local = os.getenv('FILES')
file_name = 'focos_48h_brasil.json'
path = local + '/' + file_name

# Configuration API ------------------------------------------------------------------- #

_healthChecks = HealthCheckFactory()

app = FastAPI(
    title='INPE: Programa Queimadas',
    version='1.0.0',
    description='API REST de dados abertos do INPE Programa Queimadas'
)

app.add_api_route('/api/health',
                  endpoint=healthCheckRoute(factory=_healthChecks),
                  response_model=HealthCheckSchema,
                  status_code=status.HTTP_201_CREATED,
                  summary='Verifica o conteúdo de requisões e respostas para checar se está funcionando corretamente.',
                  tags=['Health Check'])

@app.get('/focos',
         description=f'',
         response_model=List[PropertiesSchema],
         status_code=status.HTTP_200_OK,
         summary='Retorna a lista completa com todos os focos de queimadas',
         tags=['Focos de Queimadas'],
         responses={
             404: {'model': Responses, 'description': 'Code not found'},
             400: {'model': Responses, 'description': 'Code invalid.'}
         })
async def get_focos_queimadas(municipio_id: Optional[int] = Query(default=None), estado_id: Optional[int] = Query(default=None)):
    result = get_json_file(path, 'utf-8', 'features')
    if municipio_id is None and estado_id is None:
        try:
            result = get_all_results(result, 'properties')
            return result

        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')

    elif municipio_id is not None and estado_id is None:
        if len(str(municipio_id)) == 7:
            result = get_result_municipios(result, 'properties', municipio_id)
            return result

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Code {municipio_id} invalid.')

    elif municipio_id is None and estado_id is not None:
        if len(str(estado_id)) == 2:
            result = get_result_estados(result, 'properties', estado_id)
            return result

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Code {estado_id} or {municipio_id} invalid.')

@app.get('/focos/atributos/municipios',
         description=f'',
         response_model=List[MunicipiosSchema],
         status_code=status.HTTP_200_OK,
         summary='Retorna uma lista com observações únicas de todos os municípios.',
         tags=['Atributos'])
async def get_atributos_municipios():
    result = get_json_file(path, 'utf-8', 'features')
    result = get_result_atribute_municipios(result, 'properties')

    return result

@app.get('/focos/atributos/biomas',
         description=f'',
         response_model=List[BiomasSchema],
         status_code=status.HTTP_200_OK,
         summary='Retorna uma lista com observações únicas de todos os biomas.',
         tags=['Atributos'])
async def get_atributos_biomas():
    result = get_json_file(path, 'utf-8', 'features')
    result = get_result_atribute(result, 'properties', 'bioma')

    return result


@app.get('/focos/atributos/satelites',
         description=f'',
         response_model=List[SatelitesSchema],
         status_code=status.HTTP_200_OK,
         summary='Retorna uma lista com observações únicas de todos os satelites.',
         tags=['Atributos'])
async def get_atributos_satelites():
    result = get_json_file(path, 'utf-8', 'features')
    result = get_result_atribute(result, 'properties', 'satelite')

    return result


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8001, log_level='info', reload=True)
