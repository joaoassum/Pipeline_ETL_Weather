# from src.extract_data import extract_weather_data
# from src.transform_data import transform_data
# from src.load_data import load_weather_data

# import os
# from pathlib import Path
# from dotenv import load_dotenv

# import logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
# load_dotenv(env_path)
# API_KEY = os.getenv('API_KEY')

# url = f'http://api.openweathermap.org/data/2.5/weather?q=Joao Monlevade,BR&units=metric&appid={API_KEY}'
# table_name = 'jm_weather'

# def pipeline():
#     try:
#         logging.info(" -> Iniciando pipeline de ETL")
        
#         # Extract
#         extract_weather_data(url)
        
#         # Transform
#         df = transform_data()
        
#         if df.empty:
#             logging.error("Transformed DataFrame is empty. Exiting pipeline.")
#             return
        
#         # Load
#         load_weather_data(table_name, df)
        
#         logging.info(" -> Pipeline de ETL concluído com sucesso!")
    
#     except Exception as e:
#         logging.error(f"Pipeline de ETL falhou: {e}")
#         import traceback
#         traceback.print_exc()
    
# pipeline()