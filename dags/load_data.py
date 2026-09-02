from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

user = os.getenv('USUARIO_BANCO')
password = os.getenv('SENHA_BANCO')
database = os.getenv('DATABASE')
port = os.getenv('PORTA_BANCO')
host = 'postgres'
# 
def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}"
    )

engine = get_engine()

def load_weather_data(table_name:str, df: pd.DataFrame):
    df.to_sql(
        name = table_name,
        con = engine,
        if_exists = 'append',
        index = False
    )
    
    logging.info(f" -> Dados carregados na tabela {table_name} com sucesso!")
    
    df_check = pd.read_sql(
        f'SELECT * FROM {table_name}',
        con = engine
    )
    print(df_check.head())
    logging.info(f" -> Total de registros na tabela {table_name}: {len(df_check)}")