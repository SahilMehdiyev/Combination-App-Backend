# # app/config/settings.py
# from pydantic_settings import BaseSettings
# from functools import lru_cache

# class Settings(BaseSettings):
#     # App ayarları
#     app_name: str = "Combination App"
#     app_version: str = "1.0.0"
#     debug: bool = True
    
#     # Database
#     database_url: str
#     test_database_url: str = None
    
#     # Security
#     secret_key: str
#     algorithm: str = "HS256"
#     access_token_expire_minutes: int = 30
    
#     class Config:
#         env_file = ".env"
#         case_sensitive = False

# @lru_cache()
# def get_settings():
#     return Settings()