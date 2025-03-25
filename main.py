from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from middleware.auth import verify_api_key
from config import settings
from core.ollama_client import ollama_client

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 静态文件和首页不需要验证
        if request.url.path.startswith("/static") or request.url.path == "/":
            return await call_next(request)
        
        # API 接口需要验证
        api_key = request.headers.get("X-API-Key")
        if api_key != settings.API_KEY:
            return JSONResponse(
                status_code=401,
                content={"detail": "无效的API密钥"}
            )
        return await call_next(request)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置静态文件 - 移到最前面，在中间件之前
app.mount("/static", StaticFiles(directory="static"), name="static")

# 首页路由 - 在静态文件之后，中间件之前
@app.get("/")
async def read_index():
    """返回演示页面"""
    return FileResponse("static/index.html")

# API验证中间件 - 放在最后，只处理API请求
@app.middleware("http")
async def verify_api_access(request: Request, call_next):
    # 跳过静态文件和首页的验证
    if request.url.path.startswith("/static") or request.url.path == "/":
        return await call_next(request)
    
    # 验证API请求
    if request.url.path.startswith("/api") or request.url.path in ["/chat", "/generate", "/models", "/health"]:
        api_key = request.headers.get("X-API-Key")
        if api_key != settings.API_KEY:
            return JSONResponse(
                status_code=401,
                content={"detail": "无效的API密钥"}
            )
    
    return await call_next(request)

# API密钥依赖
def get_api_key_dependency():
    return Depends(verify_api_key)

# 路由注册
@app.get("/", dependencies=[Depends(verify_api_key)])
def root():
    return {"message": f"欢迎使用 {settings.PROJECT_NAME} API服务"}

@app.get("/health", dependencies=[Depends(verify_api_key)])
async def health_check():
    """检查Ollama服务的健康状态"""
    try:
        # 检查Ollama服务状态
        status = ollama_client.health_check()
        
        # 返回详细的健康状态信息
        return {
            "status": "healthy",
            "ollama_service": status,
            "api_version": settings.API_V1_STR,
            "default_model": settings.DEFAULT_MODEL,
            "available_models": settings.AVAILABLE_MODELS
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "Ollama服务连接失败"
        }

# 聊天相关的数据模型
class ChatMessage(BaseModel):
    role: str = Field(..., description="消息角色：user或assistant")
    content: str = Field(..., description="消息内容")

class ChatRequest(BaseModel):
    model: str = Field(default=settings.DEFAULT_MODEL, description="模型名称")
    messages: List[ChatMessage]
    stream: bool = Field(default=False, description="是否使用流式响应")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=1, description="采样温度")
    top_p: Optional[float] = Field(default=0.9, ge=0, le=1, description="核采样阈值")
    top_k: Optional[int] = Field(default=40, ge=0, description="保留的最高概率token数")
    presence_penalty: Optional[float] = Field(default=0.0, ge=0, le=1, description="存在惩罚")
    frequency_penalty: Optional[float] = Field(default=0.0, ge=0, le=1, description="频率惩罚")

@app.post("/chat", dependencies=[Depends(verify_api_key)])
async def chat(request: ChatRequest):
    """与模型进行对话"""
    if request.model not in settings.AVAILABLE_MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的模型。可用模型: {settings.AVAILABLE_MODELS}"
        )
    
    try:
        if request.stream:
            return StreamingResponse(
                ollama_client.chat(
                    model=request.model,
                    messages=[msg.dict() for msg in request.messages],
                    stream=True,
                    temperature=request.temperature,
                    top_p=request.top_p,
                    top_k=request.top_k,
                    presence_penalty=request.presence_penalty,
                    frequency_penalty=request.frequency_penalty
                ),
                media_type="text/event-stream"
            )
        
        return ollama_client.chat(
            model=request.model,
            messages=[msg.dict() for msg in request.messages],
            stream=False,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            presence_penalty=request.presence_penalty,
            frequency_penalty=request.frequency_penalty
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"聊天请求失败: {str(e)}"
        )

# 生成文本相关的数据模型
class GenerateMessage(BaseModel):
    prompt: str = Field(..., description="生成提示文本")
    system: Optional[str] = Field(None, description="系统提示文本")

class GenerateRequest(BaseModel):
    model: str = Field(default=settings.DEFAULT_MODEL, description="模型名称")
    message: GenerateMessage
    stream: bool = Field(default=False, description="是否使用流式响应")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=1, description="采样温度")
    top_p: Optional[float] = Field(default=0.9, ge=0, le=1, description="核采样阈值")
    top_k: Optional[int] = Field(default=40, ge=0, description="保留的最高概率token数")
    num_predict: Optional[int] = Field(default=-1, description="生成的最大token数")
    stop: Optional[List[str]] = Field(default=[], description="停止生成的标记列表")

@app.post("/generate", dependencies=[Depends(verify_api_key)])
async def generate_text(request: GenerateRequest):
    """生成文本"""
    if request.model not in settings.AVAILABLE_MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的模型。可用模型: {settings.AVAILABLE_MODELS}"
        )
    
    try:
        if request.stream:
            return StreamingResponse(
                ollama_client.generate(
                    model=request.model,
                    prompt=request.message.prompt,
                    system=request.message.system,
                    stream=True,
                    temperature=request.temperature,
                    top_p=request.top_p,
                    top_k=request.top_k,
                    num_predict=request.num_predict,
                    stop=request.stop
                ),
                media_type="text/event-stream"
            )
        
        result = ollama_client.generate(
            model=request.model,
            prompt=request.message.prompt,
            system=request.message.system,
            stream=False,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            num_predict=request.num_predict,
            stop=request.stop
        )
        
        if not result.get("success", False):
            raise Exception(result.get("error", "未知错误"))
            
        return result
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"生成请求失败: {str(e)}"
        )

@app.get("/models", dependencies=[Depends(verify_api_key)])
async def list_models():
    """获取可用模型列表"""
    try:
        models = ollama_client.list_models()
        return {
            "models": models.get("models", []),
            "default_model": settings.DEFAULT_MODEL,
            "available_models": settings.AVAILABLE_MODELS
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取模型列表失败: {str(e)}"
        )