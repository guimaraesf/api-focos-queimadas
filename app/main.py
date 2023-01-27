import os
import uvicorn
from typing import List, Optional
from utils import (get_json_file, get_result_attributes, get_result_counties, get_result_states, get_all_results, get_result_attribute_counties, get_result_attribute_states, get_result_states_counties)
from fastapi import (FastAPI, HTTPException, status, Query)
from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute
from models import (HealthCheckSchema, PropertiesSchema, MunicipiosSchema, EstadosSchema, BiomasSchema, SatelitesSchema, Responses)


# Inputs ------------------------------------------------------------------- #

local = os.getenv('FILES')  # Directory where the files will be downloaded.
file_name = 'focos_48h_brasil.json'  # File name in portal.
path = local + '/' + file_name

# Configuration API ------------------------------------------------------------------- #

_healthChecks = HealthCheckFactory()

app = FastAPI(
    title='API - Focos Queimadas',
    version='1.0.0',
    description='API REST de dados abertos disponibilizados pelo INPE - Programa Queimadas'
)

# Health Check Endpoint
app.add_api_route('/api/health',
                  endpoint=healthCheckRoute(factory=_healthChecks),
                  response_model=HealthCheckSchema,
                  status_code=status.HTTP_201_CREATED,
                  summary='Verifica a integridade das requisições',
                  tags=['Health Check'])

@app.get('/focos',
         response_model=List[PropertiesSchema],
         status_code=status.HTTP_200_OK,
         summary=f'Retorna dos dados de focos de calor nas últimas {file_name[6:8]} horas',
         tags=['Focos de Queimadas'],
         responses={
             400: {'model': Responses, 'description': 'Code invalid.'},
             404: {'model': Responses, 'description': 'Code not found'},
             422: {'model': Responses, 'description': 'Codes do not match.'}
         })
async def get_focos(municipio_id: Optional[int] = Query(default=None), estado_id: Optional[int] = Query(default=None)):
    result = get_json_file(path, 'utf-8', 'features')

    if municipio_id is None and estado_id is None:
        try:
            result = get_all_results(result, 'properties')
            return result

        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')

    if municipio_id is not None and estado_id is None:
        try:
            if len(str(municipio_id)) == 7:
                result = get_result_counties(result, 'properties', municipio_id)
                return result

            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f'Code {municipio_id} invalid.')
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')

    if municipio_id is None and estado_id is not None:
        try:
            if len(str(estado_id)) == 2:
                result = get_result_states(result, 'properties', estado_id)
                return result
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f'Code {municipio_id} invalid.')
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')

    if municipio_id is not None and estado_id is not None:
        if len(str(municipio_id)) == 7 and len(str(estado_id)) == 2:
            if str(municipio_id)[:2] == str(estado_id):
                result = get_result_states_counties(result, 'properties', estado_id, municipio_id)
                return result
            else:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    detail=f'Codes {estado_id} and {municipio_id} not match. The first 2 digits of the county must match')
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Codes {estado_id} or {municipio_id} invalid.')


@app.get('/focos/atributos/municipios',
         response_model=List[MunicipiosSchema],
         status_code=status.HTTP_200_OK,
         summary='Retorno dos dados de observações únicas de municípios.',
         tags=['Atributos'])
async def get_attribute_counties():
    try:
        result = get_json_file(path, 'utf-8', 'features')
        result = get_result_attribute_counties(result, 'properties')
        return result
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')

@app.get('/focos/atributos/estados',
         response_model=List[EstadosSchema],
         status_code=status.HTTP_200_OK,
         summary='Retorno dos dados de observações únicas de estados.',
         tags=['Atributos'])
async def get_attribute_states():
    try:
        result = get_json_file(path, 'utf-8', 'features')
        result = get_result_attribute_states(result, 'properties')
        return result

    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')

@app.get('/focos/atributos/biomas',
         response_model=List[BiomasSchema],
         status_code=status.HTTP_200_OK,
         summary='Retorno dos dados de observações únicas de biomas.',
         tags=['Atributos'])
async def get_attribute_biomes():
        try:
            result = get_json_file(path, 'utf-8', 'features')
            result = get_result_attributes(result, 'properties', 'bioma')
            return result

        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')


@app.get('/focos/atributos/satelites',
         response_model=List[SatelitesSchema],
         status_code=status.HTTP_200_OK,
         summary='Retorno dos dados de observações únicas de satélites.',
         tags=['Atributos'])
async def get_attribute_satellites():
    try:
        result = get_json_file(path, 'utf-8', 'features')
        result = get_result_attributes(result, 'properties', 'satelite')
        return result

    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8001, log_level='info', reload=True)
