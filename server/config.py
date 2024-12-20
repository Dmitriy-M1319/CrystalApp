from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_ip: str = ""
    database_port: int = 0
    database_user: str = ""
    database_password: str = ""
    database_name: str = ""
    report_server_address: str = ""
    reports_storage: str = ""
    
    model_config = SettingsConfigDict(env_file=".env")