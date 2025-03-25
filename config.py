from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Dict
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):
    # API配置
    API_V1_STR: str = Field(default="/api/v1", description="API版本路径前缀")
    PROJECT_NAME: str = Field(default="OllamaHub", description="项目名称")
    API_KEY: str = Field(default="ap-czt-api", description="API密钥")  # 添加这行
    
    # Ollama服务配置
    OLLAMA_API_URL: str = Field(default="http://127.0.0.1:11434", description="Ollama API服务地址")
    DEFAULT_MODEL: str = Field(default="deepseek-r1:14b", description="默认模型配置")
    AVAILABLE_MODELS: List[str] = Field(
        default=["deepseek-r1:14b"],
        description="可用模型列表"
    )
    
    # 安全配置
    SECRET_KEY: str = Field(
        default="3d6f45a5c2786745fda1288beb65a68852137a828a2f2b29c4e9e8a1d9b5c8f7",
        description="JWT加密密钥"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60,
        description="访问令牌过期时间（分钟）"
    )
    
    # API密钥配置
    API_KEYS: Dict[str, str] = Field(
        default={
            "default": "ap-czt-api",
            "user1": "ak-001"
        },
        description="API密钥字典，用于API访问认证"
    )
    
    # 知识库配置
    KNOWLEDGE_BASE_PATH: str = Field(default="knowledge_base", description="知识库文件存储路径")
    VECTOR_DB_PATH: str = Field(default="vector_db", description="向量数据库存储路径")
    
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env"
    )

settings = Settings()