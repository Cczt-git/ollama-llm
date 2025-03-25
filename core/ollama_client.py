import requests
from typing import Dict, Any, Optional
from config import settings

# Ollama API客户端类，用于与Ollama服务进行交互
class OllamaClient:
    def __init__(self):
        # 初始化Ollama API的基础URL
        self.base_url = settings.OLLAMA_API_URL
        
    def _make_request(self, endpoint: str, method: str = "POST", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """发送HTTP请求到Ollama API
        
        Args:
            endpoint: API端点路径
            method: HTTP请求方法，默认为POST
            data: 请求数据，可选
            
        Returns:
            Dict[str, Any]: API响应的JSON数据
            
        Raises:
            Exception: 当API请求失败时抛出异常
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API请求失败: {str(e)}")
    
    def list_models(self) -> Dict[str, Any]:
        """获取可用的模型列表
        
        Returns:
            Dict[str, Any]: 包含可用模型信息的字典
        """
        return self._make_request("api/tags", method="GET")
    
    def generate(self, model: str, prompt: str, system: Optional[str] = None, stream: bool = False, **kwargs) -> Dict[str, Any]:
        """生成文本响应
        
        Args:
            model: 使用的模型名称
            prompt: 输入提示文本
            system: 系统提示文本，可选
            stream: 是否使用流式响应
            **kwargs: 其他可选参数
            
        Returns:
            Dict[str, Any]: 生成的文本响应
        """
        data = {
            "model": model,
            "prompt": prompt,
            "stream": stream,  # stream 参数应该在顶层
            "system": system if system else None,
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.9),
            "top_k": kwargs.get("top_k", 40),
            "num_predict": kwargs.get("num_predict", -1),
            "stop": kwargs.get("stop", [])
        }
        
        if stream:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=data,
                stream=True
            )
            response.raise_for_status()
            return response.iter_lines()
            
        try:
            response = self._make_request("api/generate", data=data)
            return {
                "success": True,
                "response": response.get("response", ""),
                "model": model,
                "total_duration": response.get("total_duration", 0),
                "load_duration": response.get("load_duration", 0),
                "prompt_eval_count": response.get("prompt_eval_count", 0),
                "eval_count": response.get("eval_count", 0),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": model
            }
    
    def chat(self, model: str, messages: list, stream: bool = False, **kwargs) -> Dict[str, Any]:
        """进行对话交互
        
        Args:
            model: 使用的模型名称
            messages: 对话消息列表
            stream: 是否使用流式响应
            **kwargs: 其他可选参数，如temperature、top_p等
            
        Returns:
            Dict[str, Any]: 对话响应
        """
        data = {
            "model": model,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9),
                "top_k": kwargs.get("top_k", 40),
                "num_ctx": kwargs.get("num_ctx", 4096),
                "num_predict": kwargs.get("num_predict", -1),
                "stop": kwargs.get("stop", []),
                "presence_penalty": kwargs.get("presence_penalty", 0.0),
                "frequency_penalty": kwargs.get("frequency_penalty", 0.0),
                "repeat_penalty": kwargs.get("repeat_penalty", 1.1),
                "tfs_z": kwargs.get("tfs_z", 1.0),
                "mirostat": kwargs.get("mirostat", 0),
                "mirostat_tau": kwargs.get("mirostat_tau", 5.0),
                "mirostat_eta": kwargs.get("mirostat_eta", 0.1),
            }
        }
        
        # 如果是流式响应，使用不同的处理逻辑
        if stream:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=data,
                stream=True
            )
            response.raise_for_status()
            return response.iter_lines()
            
        return self._make_request("api/chat", data=data)
    
    def embeddings(self, model: str, text: str) -> Dict[str, Any]:
        """获取文本的嵌入向量
        
        Args:
            model: 使用的模型名称
            text: 需要获取嵌入向量的文本
            
        Returns:
            Dict[str, Any]: 包含嵌入向量的响应
        """
        data = {
            "model": model,
            "prompt": text
        }
        return self._make_request("api/embeddings", data=data)
    
    def health_check(self) -> Dict[str, Any]:
        """检查Ollama服务的健康状态
        
        Returns:
            Dict[str, Any]: 包含服务状态和可用模型信息的响应
        """
        try:
            # 尝试获取模型列表来检查服务是否可用
            models = self.list_models()
            return {
                "status": "healthy",
                "message": "Ollama服务运行正常",
                "available_models": models.get("models", [])
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Ollama服务连接失败: {str(e)}",
                "available_models": []
            }

# 创建全局Ollama客户端实例
ollama_client = OllamaClient()