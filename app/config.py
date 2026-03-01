from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr

class Settings(BaseSettings):
    # Database
    DB_HOSTNAME: str
    DB_USERNAME: str
    DB_PWD: str
    DB_NAME: str
    DB_PORT: str

    # Admin
    ADMIN_EMAIL: EmailStr
    ADMIN_PWD: str

    # Security
    ALGORITHM: str
    SECRET_KEY: str

    #verification with RESEND
    EMAIL_API_KEY_RESEND : str
    DOMAIN_NAME : str

    #sendgrid email functionoality
    SENDGRID_API_KEY : str
    SENDGRID_EMAIL: str

    @property
    def cleaned_db_pwd(self):
        return self.DB_PWD.strip()

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )

# One instance to rule them all
settings = Settings()