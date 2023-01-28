import json
from collections import OrderedDict

# Functions ------------------------------------------------------------------- #

def get_json_file(file, encoding: str, key: str) -> json:
    """Read json file and select a key"""
    with open(file, encoding=encoding) as data:
        data = json.load(data)
        data = data[key]

    return data


def get_all_results(file: json, key: str) -> json:
    """Returns all available results"""
    my_list = []
    for i in range(len(file)):
        my_list.append(file[i][key])
    return my_list


def get_result_attribute_counties(file: json, key: str) -> json:
    """Returns the unique observations of cities"""
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


def get_result_attribute_states(file: json, key: str) -> json:
    """Returns the unique observations of cities"""
    my_list = []
    key_order = ['pais_id', 'pais', 'estado_id', 'estado']
    for i in range(len(file)):
        items = file[i][key].items()
        my_dict = {k: v for k, v in items
                   if k.endswith('pais_id')
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


def get_result_attributes(file: json, key: str, attribute: str) -> json:
    """Returns the unique observations of any attribute"""
    my_list = []
    for i in range(len(file)):
        items = file[i][key].items()
        my_dict = {k: v for k, v in items if k.endswith(attribute)}
        my_list = [my_list[i] for i in range(len(my_list)) if i == my_list.index(my_list[i])]
        my_list.append(my_dict)
    del my_list[-1]

    return my_list

def get_result_counties(file: json, key: str, municipio_id: int) -> json:
    """Returns the results from the filter by city code"""
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

def get_result_states(file: json, key: str, estado_id: int) -> json:
    """Returns the results from the filter by state code"""
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


def get_result_states_counties(file: json, key: str, estado_id: int, municipio_id: int) -> json:
    """Returns the results from the filter by state code"""
    my_list = []
    keys = ['id', 'longitude', 'latitude', 'data_hora_gmt', 'satelite',
            'municipio', 'estado', 'pais', 'municipio_id', 'estado_id', 'pais_id',
            'numero_dias_sem_chuva', 'precipitacao', 'risco_fogo', 'bioma']

    for i in range(len(file)):
        items = file[i][key].items()
        my_dict = {k: v for k, v in items if k in keys}
        for k, v in my_dict.items():
            if 'estado_id' in k and estado_id == v:
                for k, v in my_dict.items():
                    if 'municipio_id' in k and municipio_id == v:
                        my_list.append(my_dict)

    return my_list

# def get_result_counties_count(file: json, key: str, municipio_id: int) -> json:
#     """Returns the unique observations of cities"""
#     my_list = []
#     count = 0
#     key_order = ['estado_id', 'estado', 'municipio_id', 'municipio']
#     for i in range(len(file)):
#         items = file[i][key].items()
#         values = file[i][key].values()
#         my_dict = {k: v for k, v in items
#                    if k.endswith('municipio_id')
#                    or k.endswith('municipio')
#                    or k.endswith('estado_id')
#                    or k.startswith('estado')}
#         my_dict = OrderedDict(my_dict)
#         for k in key_order:
#             my_dict.move_to_end(k)
#         my_list = [my_list[i] for i in range(len(my_list)) if i == my_list.index(my_list[i])]
#         for v in values:
#             count += 1
#             my_dict['contagem'] = count
#         my_list.append(my_dict)
#     del my_list[-1]
#
#     return my_list