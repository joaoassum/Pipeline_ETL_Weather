import pandas as pd
from pathlib import Path
import json

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json'
columns_to_drop = ['weather', 'weather_icon']
columns_to_rename = {
    'base': 'weather_base',
    'visibility': 'weather_visibility',
    'dt': 'weather_dt',
    'timezone' : 'timezone',
    'id': 'city_id',
    'name': 'city_name', 
    'cod': 'cod', 
    'coord.lon': 'longitude', 
    'coord.lat': 'latitude', 
    'main.temp': 'temperatuda', 
    'main.feels_like': 'feels_like',
    'main.temp_min': 'temp_min', 
    'main.temp_max': 'temp_max', 
    'main.pressure': 'pressure', 
    'main.humidity': 'humidity',
    'main.sea_level': 'sea_level', 
    'main.grnd_level': 'ground_level', 
    'wind.speed': 'wind_speed', 
    'wind.deg': 'wind_degree',
    'wind.gust': 'wind_gust',
    'rain.1h': 'rain_1h',
    'clouds.all': 'clouds_all',
    'sys.country': 'sys_country',
    'sys.sunrise': 'sys_sunrise',
    'sys.sunset': 'sys_sunset',
    'weather_id': 'weather_id',
    'weather_main': 'weather_main',
    'weather_description': 'weather_description'
    }
columns_to_normalize_datetime = ['sys_sunrise', 'sys_sunset', 'weather_dt']

def create_dataframe(path_name:str) -> pd.DataFrame:
    logging.info(" -> Criando DataFrame do arquivo JSON")
    path = path_name
    
    if not path.exists():
        raise FileNotFoundError(f"The file {path} does not exist.")

    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    
    logging.info(f" -> DataFrame com {len(df)} llinhas foi criado")
    
    return df

def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
    logging.info(" -> Normalizando colunas do DataFrame")
    
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))
    
    df_weather = df_weather.rename(columns = {
        'id' : 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })
    
    df = pd.concat([df, df_weather], axis=1)
    logging.info(f"Coluna 'weather' normalizada com sucesso - {len(df.columns)} colunas")
    
    return df
    
def drop_columns(df: pd.DataFrame, columns_to_drop: list[str]) -> pd.DataFrame: 
    logging.info(f" -> Dropando colunas: {columns_to_drop}")
    
    df = df.drop(columns= columns_to_drop)
    
    logging.info(f"Colunas dropadas com sucesso - {len(df.columns)} colunas restantes")
    
    return df

def rename_columns(df: pd.DataFrame, columns_to_rename:dict[str, str]) -> pd.DataFrame:
    logging.info(f" -> Renomeando colunas: {columns_to_rename}")
    
    df = df.rename(columns=columns_to_rename)
    
    return df

def normalize_datetime_columns(df: pd.DataFrame, columns_name:list[str]) -> pd.DataFrame:
    logging.info(" -> Normalizando colunas de data e hora")
    
    for name in  columns_name:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')
        
    return df

def transform_weather_data() -> pd.DataFrame:
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df, columns_to_drop)
    df = rename_columns(df, columns_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)
    return df

# print(transform_data().head())