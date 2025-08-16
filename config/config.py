from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("settings.env")


class config(BaseModel):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")


# Create config instance with environment variables
config = config(openai_api_key=os.getenv("OPENAI_API_KEY"))
