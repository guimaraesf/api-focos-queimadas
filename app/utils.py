import json
from collections import OrderedDict

# Functions ------------------------------------------------------------------- #

def get_json_file(file, encoding: str, key: str) -> json:
    """Após ler o arquivo json, o formata para o padrão necessário """
    with open(file, encoding=encoding) as data:
        data = json.load(data)
        data = data[key]

    return data


def get_result_municipio(file: json, municipio_id: int, key: str) -> json:
    lista = []
    length_id = len(str(municipio_id))
    if length_id == 7:
        for i in range(len(file)):
            values = file[i][key].values()
            if municipio_id in values:
                lista.append(file[i][key])
        return lista


def get_all_results(file: json, key: str) -> json:
    lista = []
    for i in range(len(file)):
        lista.append(file[i][key])
    return lista


def get_result_estados(file: json, estado_id: int, key: str):
    _list = []
    length_id = len(str(estado_id))
    if length_id == 2:
        for i in range(len(file)):
            values = file[i][key].values()
            print(values)
            if estado_id in values:
                _list.append(file[i][key])
        return _list


def get_result_atribute_municipios(file: json, key: str) -> json:
    my_list = []
    key_order = ['pais_id', 'pais', 'estado_id', 'estado', 'municipio_id', 'municipio']
    for i in range(len(file)):
        items = file[i][key].items()
        my_dict = {k: v for k, v in items
                   if k.endswith('_id')
                   or k.startswith('pais')
                   or k.startswith('estado')
                   or k.startswith('municipio')}
        my_dict = OrderedDict(my_dict)
        for k in key_order:
            my_dict.move_to_end(k)
        my_list = [my_list[i] for i in range(len(my_list)) if i == my_list.index(my_list[i])]
        my_list.append(my_dict)
    del my_list[-1]

    return my_list


# Corrigir, pois os estados estão se repetindo.
def get_result_atribute_estados(file: json, key: str) -> json:
    my_list = []
    key_order = ['pais_id', 'pais', 'estado_id', 'estado']
    for i in range(len(file)):
        items = file[i][key].items()
        my_dict = {k: v for k, v in items
                   or k.endswith('pais_id')
                   or k.endswith('pais')
                   or k.endswith('estado_id')
                   or k.startswith('estado')}
        my_dict = OrderedDict(my_dict)
        for k in key_order:
            my_dict.move_to_end(k)
        my_list = [my_list[i] for i in range(len(my_list)) if i == my_list.index(my_list[i])]
        my_list.append(my_dict)
    del my_list[-1]

    return my_list


def get_result_atribute(file: json, key: str, atribute: str) -> json:
    my_list = []
    for i in range(len(file)):
        items = file[i][key].items()
        my_dict = {k: v for k, v in items if k.endswith(atribute)}
        my_list = [my_list[i] for i in range(len(my_list)) if i == my_list.index(my_list[i])]
        my_list.append(my_dict)
    del my_list[-1]

    return my_list

def get_result_municipios(file: json, key: str, municipio_id: int) -> json:
    my_list = []
    keys = ['id', 'longitude', 'latitude', 'data_hora_gmt', 'satelite',
            'municipio', 'estado', 'pais', 'municipio_id', 'estado_id', 'pais_id',
            'numero_dias_sem_chuva', 'precipitacao', 'risco_fogo', 'bioma']

    for i in range(len(file)):
        items = file[i][key].items()
        my_dict = {k: v for k, v in items if k in keys}
        for k, v in my_dict.items():
            if municipio_id == v:
                my_list.append(my_dict)

    return my_list

def get_result_estados(file: json, key: str, estado_id: int) -> json:
    my_list = []
    keys = ['id', 'longitude', 'latitude', 'data_hora_gmt', 'satelite',
            'municipio', 'estado', 'pais', 'municipio_id', 'estado_id', 'pais_id',
            'numero_dias_sem_chuva', 'precipitacao', 'risco_fogo', 'bioma']

    for i in range(len(file)):
        items = file[i][key].items()
        my_dict = {k: v for k, v in items if k in keys}
        for k, v in my_dict.items():
            if 'estado_id' in k and estado_id == v:
                my_list.append(my_dict)

    return my_list