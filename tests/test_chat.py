import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
import time

def chat_with_model(message, model="deepseek-r1:14b", stream=True, messages=None):
    """与模型进行对话"""
    url = "http://localhost:8000/chat"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "ap-czt-api"
    }
    
    if messages is None:
        messages = []
    messages.append({"role": "user", "content": message})
    
    data = {
        "model": model,
        "messages": messages,
        "stream": stream,
        "temperature": 0.7
    }
    
    try:
        if stream:
            response = requests.post(url, headers=headers, json=data, stream=True)
            assistant_message = ""
            # print("发送请求...")
            response = requests.post(url, headers=headers, json=data, stream=True)
            # print(f"服务器响应状态码: {response.status_code}")
            # print("请求头:", response.headers)  # 添加响应头信息
            
            last_content = ""  # 用于存储上一次的内容
            for line in response.iter_lines():
                if line:
                    try:
                        line_str = line.decode('utf-8')
                        # 分割多个JSON对象
                        json_strings = line_str.split('}{')
                        for i, json_str in enumerate(json_strings):
                            # 重新添加花括号
                            if i > 0:
                                json_str = '{' + json_str
                            if i < len(json_strings) - 1:
                                json_str = json_str + '}'
                            
                            try:
                                chunk = json.loads(json_str)
                                if 'message' in chunk and 'content' in chunk['message']:
                                    content = chunk['message']['content'].strip()
                                    if not content:
                                        continue
                                    # 处理换行符
                                    if content == '<think>':
                                        print('\n<think>\n', end='', flush=True)
                                    elif content == '</think>':
                                        print('\n</think>\n', end='', flush=True)
                                    else:
                                        print(content, end='', flush=True)
                                    time.sleep(0.05)  # 每个字符添加延迟
                            except json.JSONDecodeError:
                                continue
                    except Exception as e:
                        continue
            messages.append({"role": "assistant", "content": assistant_message})
            return messages
            
        else:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            content = result.get('message', {}).get('content', '')
            # 移除think标签内容
            if '<think>' in content:
                content = content.split('</think>')[-1].strip()
            print(content)
            
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return messages

if __name__ == "__main__":
    messages = []
    while True:
        user_input = input("\n请输入您的问题（输入'退出'结束对话）：")
        if user_input.lower() in ['退出', 'quit', 'exit']:
            break
        messages = chat_with_model(user_input, stream=True, messages=messages)
    
    
