# import os
# from pydantic import BaseSettings

# class Settings(BaseSettings):
#     APP_NAME: str = "chat-service"
#     ENV: str = "dev"

#     # Provider switch
#     LLM_PROVIDER: str = "openai"  # openai | mock | others

#     # OpenAI
#     OPENAI_API_KEY: str | None = None
#     OPENAI_MODEL: str = "gpt-4o-mini"

#     class Config:
#         env_file = ".env"

# settings = Settings()



from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. Define settings model
class Settings(BaseSettings):
    # These will be loaded from env vars or .env file
    HOST: str = "localhost"
    PORT: int = 8000
    LLM_PROVIDER: str | None = None

    # OpenAI
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # vLLM
    VLLM_BASE_URL: str | None = None
    VLLM_MODEL: str | None = None
    # Claude
    ANTHROPIC_API_KEY: str | None = None
    CLAUDE_MODEL: str = "claude-3-haiku-20240307"

    # 2. Configure to read from a .env file
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )

# 3. Instantiate to load automatically
settings = Settings()
print(settings.HOST)
print(settings.LLM_PROVIDER)