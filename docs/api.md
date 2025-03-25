# API 文档

## 基础信息

- 基础URL: `/api/v1`
- 认证方式: API密钥认证（在请求头中添加 `X-API-Key`）

## API 接口

### 1. 获取模型列表

```http
GET /models
```

获取所有可用的模型列表。

**响应示例：**
```json
{
    "models": [
        "deepseek-r1:14b",
        "deepseek-r1:8b"
    ]
}
```

### 2. 生成文本

```http
POST /generate
```

使用指定模型生成文本响应。

**请求参数：**
```json
{
    "model": "deepseek-r1:14b",
    "prompt": "你好，请介绍一下自己",
    "system": "你是一个AI助手",
    "stream": false,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "num_predict": -1,
    "stop": []
}
```

**响应示例：**
```json
{
    "success": true,
    "response": "你好！我是一个AI助手...",
    "model": "deepseek-r1:14b",
    "total_duration": 1234,
    "load_duration": 100,
    "prompt_eval_count": 50,
    "eval_count": 200
}
```

### 3. 对话接口

```http
POST /chat
```

进行多轮对话交互。

**请求参数：**
```json
{
    "model": "deepseek-r1:14b",
    "messages": [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！有什么我可以帮你的吗？"},
        {"role": "user", "content": "请介绍一下自己"}
    ],
    "stream": false,
    "options": {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "num_ctx": 4096,
        "num_predict": -1,
        "stop": [],
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
        "repeat_penalty": 1.1
    }
}
```

### 4. 获取文本向量

```http
POST /embeddings
```

获取文本的嵌入向量表示。

**请求参数：**
```json
{
    "model": "deepseek-r1:14b",
    "text": "需要获取向量的文本内容"
}
```

### 5. 健康检查

```http
GET /health
```

检查服务的运行状态。

**响应示例：**
```json
{
    "status": "healthy",
    "message": "Ollama服务运行正常",
    "available_models": ["deepseek-r1:14b", "deepseek-r1:8b"]
}
```

## 错误处理

当API调用发生错误时，会返回相应的HTTP状态码和错误信息：

```json
{
    "success": false,
    "error": "错误信息描述"
}
```

常见HTTP状态码：
- 200: 请求成功
- 400: 请求参数错误
- 401: 认证失败
- 404: 资源不存在
- 500: 服务器内部错误