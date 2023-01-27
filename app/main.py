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
    title='INPE: Programa Queimadas',
    version='1.0.0',
    description='API REST de dados abertos do INPE Programa Queimadas'
)

# Health Check Endpoint
app.add_api_route('/api/health',
                  endpoint=healthCheckRoute(factory=_healthChecks),
                  response_model=HealthCheckSchema,
                  status_code=status.HTTP_201_CREATED,
                  summary='Verifica a integridade das requisições',
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
            result = get_result_states_counties(result, 'properties', estado_id, municipio_id)
            return result
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Code {estado_id} or {municipio_id} invalid.')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Code {estado_id} or {municipio_id} not found.')

@app.get('/focos/atributos/municipios',
         description=f'',
         response_model=List[MunicipiosSchema],
         status_code=status.HTTP_200_OK,
         summary='Retorna uma lista com observações únicas de todos os municípios.',
         tags=['Atributos'])
async def get_attribute_counties():
    result = get_json_file(path, 'utf-8', 'features')
    result = get_result_attribute_counties(result, 'properties')

    return result

@app.get('/focos/atributos/estados',
         description=f'',
         response_model=List[EstadosSchema],
         status_code=status.HTTP_200_OK,
         summary='Retorna uma lista com observações únicas de todos os municípios.',
         tags=['Atributos'])
async def get_attribute_states():
    result = get_json_file(path, 'utf-8', 'features')
    result = get_result_attribute_states(result, 'properties')

    return result


@app.get('/focos/atributos/biomas',
         description=f'',
         response_model=List[BiomasSchema],
         status_code=status.HTTP_200_OK,
         summary='Retorna uma lista com observações únicas de todos os biomas.',
         tags=['Atributos'])
async def get_attribute_biomes():
    result = get_json_file(path, 'utf-8', 'features')
    result = get_result_attributes(result, 'properties', 'bioma')

    return result


@app.get('/focos/atributos/satelites',
         description=f'',
         response_model=List[SatelitesSchema],
         status_code=status.HTTP_200_OK,
         summary='Retorna uma lista com observações únicas de todos os satelites.',
         tags=['Atributos'])
async def get_attribute_satellites():
    result = get_json_file(path, 'utf-8', 'features')
    result = get_result_attributes(result, 'properties', 'satelite')

    return result


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8001, log_level='info', reload=True)
