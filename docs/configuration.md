# 配置说明

## 基础配置
在 `config.py` 中配置：
```python
# API配置
API_V1_STR = "/api/v1"  # API版本路径前缀
PROJECT_NAME = "OllamaHub"  # 项目名称
API_KEY = "ap-czt-api"  # API密钥

# Ollama服务配置
OLLAMA_API_URL = "http://127.0.0.1:11434"  # Ollama API服务地址
DEFAULT_MODEL = "deepseek-r1:14b"  # 默认模型配置
AVAILABLE_MODELS = ["deepseek-r1:14b"]  # 可用模型列表

# 安全配置
SECRET_KEY = "3d6f45a5c2786745fda1288beb65a68852137a828a2f2b29c4e9e8a1d9b5c8f7"  # JWT加密密钥
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 访问令牌过期时间（分钟）

# API密钥配置
API_KEYS = {  # API密钥字典，用于API访问认证
    "default": "ap-czt-api",
    "user1": "ak-001"
}

# 知识库配置
KNOWLEDGE_BASE_PATH = "knowledge_base"  # 知识库文件存储路径
VECTOR_DB_PATH = "vector_db"  # 向量数据库存储路径
```

## 配置说明

### API配置
- `API_V1_STR`: API版本路径前缀，用于API路由的版本控制
- `PROJECT_NAME`: 项目名称
- `API_KEY`: 默认API密钥

### Ollama服务配置
- `OLLAMA_API_URL`: Ollama API服务地址，默认为本地服务
- `DEFAULT_MODEL`: 默认使用的模型名称
- `AVAILABLE_MODELS`: 系统中可用的模型列表

### 安全配置
- `SECRET_KEY`: JWT令牌加密密钥
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 访问令牌的有效期（分钟）

### API密钥配置
- `API_KEYS`: API密钥字典，用于API访问认证
  - 可配置多个API密钥，每个密钥对应一个用户

### 知识库配置
- `KNOWLEDGE_BASE_PATH`: 知识库文件的存储路径
- `VECTOR_DB_PATH`: 向量数据库的存储路径

## 环境变量配置
所有配置项都可以通过环境变量进行覆盖。环境变量的名称与配置项名称相同。例如：
```bash
OLLAMA_API_URL=http://localhost:11434
DEFAULT_MODEL=deepseek-r1:14b
```

可以通过创建 `.env` 文件来设置环境变量：
```bash
# API配置
API_V1_STR=/api/v1
PROJECT_NAME=OllamaHub

# Ollama服务配置
OLLAMA_API_URL=http://127.0.0.1:11434
DEFAULT_MODEL=deepseek-r1:14b
```