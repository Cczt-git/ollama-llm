# 部署指南

## 环境要求

- Python 3.8+
- Ollama 服务运行中
- 已安装所需模型

## 安装步骤

1. 安装依赖包
```bash
pip install fastapi uvicorn pydantic requests
```

2. 配置环境
- 复制项目根目录下的 `.env.example` 文件（如果存在）为 `.env`
- 根据实际情况修改 `.env` 文件中的配置项
- 主要配置项包括：
  - OLLAMA_API_URL：Ollama服务地址
  - DEFAULT_MODEL：默认使用的模型
  - API_KEY：API访问密钥

## 启动服务

1. 确保Ollama服务已启动

2. 启动OllamaHub服务
```bash
python run.py
```

默认情况下，服务将在以下地址启动：
- 主机：0.0.0.0
- 端口：8000

可以通过浏览器访问 http://localhost:8000 来查看服务是否正常运行。

## 配置说明

详细的配置说明请参考 [配置说明文档](configuration.md)。

## 常见问题

1. 服务无法启动
- 检查端口是否被占用
- 确认Python版本是否满足要求
- 检查依赖包是否安装完整

2. 无法连接到Ollama服务
- 确认Ollama服务是否正常运行
- 检查OLLAMA_API_URL配置是否正确
- 确认网络连接是否正常

3. API调用失败
- 检查API密钥是否正确
- 确认请求参数是否符合要求
- 查看服务日志获取详细错误信息