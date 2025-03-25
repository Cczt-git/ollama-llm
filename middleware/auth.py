from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from typing import Optional

from config import settings

# 定义API密钥请求头，用于API认证
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)) -> Optional[str]:
    """验证并获取API密钥
    
    Args:
        api_key_header: 从请求头中获取的API密钥
        
    Returns:
        Optional[str]: 有效的API密钥
        
    Raises:
        HTTPException: 当API密钥无效时抛出401未授权异常
    """
    if api_key_header in settings.API_KEYS.values():
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的API密钥"
    )

def verify_api_key(api_key: str = Security(get_api_key)):
    """验证API密钥的依赖函数
    
    Args:
        api_key: 通过get_api_key函数验证的API密钥
        
    Returns:
        str: 验证通过的API密钥
    """
    return api_key