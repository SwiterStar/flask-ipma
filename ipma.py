import requests
from datetime import datetime

URL_CIDADES = "https://api.ipma.pt/open-data/distrits-islands.json"
URL_PREV = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{gid}.json"
URL_TYPES = "https://api.ipma.pt/open-data/weather-type-classe.json"

def _mapa_cidades():
    '''
    Mapeia cidades para os seus IDS globais.
    retorna: um dicionario onde as chaves são os nomes das cidades e os valores são os ids globais
    '''
    try:
        dados=requests.get(URL_CIDADES,timeout=10).json()['data']
        return {i['local']:i['globalIdLocal'] for i in dados}
    except Exception as e:
        print(f'Erro ao obter dados das Cidades: {e}')
        return {}

def _mapa_icons():
    '''
    Mapeia os tipos de tempo para descrição e nomes dos ficheiros dos icones
    Retorna: {id_tipo_tempo:(descrição_tempo,icone_tempo)}
    '''
    try: 
        dados=requests.get(URL_TYPES,timeout=10).json()['data']
        return{
            (i['idweatherType']):
            (i['descWeatherTypePT'],
             f'w_ic_d_{str(i['idWeatherType']).zfill(2)}.svg') 
            for i in dados}
    except Exception as e:
        print(f'Erro ao obter dados de tempo: {e}')
        return {}

CIDADES=_mapa_cidades()
ICONES=_mapa_icons()

def previsao_por_cidade(nome_cidade):
    '''
    Obter a previsao do tempo para uma cidade especifica

    Args:
        nome_cidade (str): o nome da cidade para a qual queremos obter a previsao do tempo
    Retorna:
        lista: uma lista de dicionarios com a previsao diaria incluindo a descriçao e o icone
    Lança:
        ValueError se a cidade nao for encontrada
        Exception se ocorrer um erro na chamada da API
    '''
    gid=CIDADES.get(nome_cidade.title())
    if gid is None:
        raise ValueError('Cidade não encontrada')

    try:
        dados=requests.get(URL_PREV.format(gid=gid),timeout=10).json()['data']
    except Exception as e:
        print(f'Erro ao obter a previsão: {e}')
        raise 
    
    for i in dados:
        try:
            weather_type=int(i.get('idWeatherType',0))
            desc,icon_file=ICONES.get(weather_type,('-','icon-fallback.svg'))
            
        except Exception as e:
            print(f'Erro ao obter a previsão: {e}')
            raise 



