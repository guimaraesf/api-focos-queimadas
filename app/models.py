from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any


class HealthCheckSchema(BaseModel):
    status: str
    totalTimeTaken: str
    entities: list


class PropertiesSchema(BaseModel):
    id: str
    longitude: float
    latitude: float
    data_hora_gmt: datetime
    satelite: str
    municipio: str
    estado: str
    pais: str
    municipio_id: int = Field(default=..., description='Código de município do IBGE')
    estado_id: int = Field(default=..., description='Código de estado do IBGE')
    pais_id: int
    numero_dias_sem_chuva: Any
    precipitacao: Any
    risco_fogo: Any
    bioma: Any


class MunicipiosSchema(BaseModel):
    pais_id: int
    pais: str
    estado_id: int = Field(default=..., description='Código de estado do IBGE')
    estado: str
    municipio_id: int = Field(default=..., description='Código de município do IBGE')
    municipio: str


class EstadosSchema(BaseModel):
    pais_id: int
    pais: str
    estado_id: int = Field(default=..., description='Código de estado do IBGE')
    estado: str


class BiomasSchema(BaseModel):
    bioma: str


class SatelitesSchema(BaseModel):
    satelite: str


class Responses(BaseModel):
    message: str