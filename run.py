import uvicorn
import argparse
from config import settings
import webbrowser
import time
import threading

def open_browser():
    """延迟2秒后打开浏览器"""
    time.sleep(2)
    webbrowser.open(f"http://127.0.0.1:8000")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='OllamaHub API服务')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='服务监听地址')
    parser.add_argument('--port', type=int, default=8000, help='服务端口')
    parser.add_argument('--reload', action='store_true', help='是否启用热重载')
    parser.add_argument('--workers', type=int, default=1, help='工作进程数')
    
    args = parser.parse_args()
    
    print(f"启动 {settings.PROJECT_NAME} 服务...")
    print(f"API文档: http://{args.host}:{args.port}/docs")
    print(f"演示页面: http://{args.host}:{args.port}")
    
    # 启动浏览器线程
    threading.Thread(target=open_browser).start()
    
    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers
    )