from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class DbSetting(BaseSettings):
    DB_HOSTNAME : str
    DB_USERNAME : str
    DB_PWD: str
    DB_NAME : str
    DB_PORT : str
    
    @property
    def cleaned_pwd(self):
        return self.DB_PWD.strip()


    model_config = SettingsConfigDict(
        env_file=os.path.join(os.getcwd(), ".env"),
        extra="ignore"
    )

DB_Setting = DbSetting()