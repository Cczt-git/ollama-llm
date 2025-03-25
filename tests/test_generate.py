import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json

def generate_text(prompt, system=None, model="deepseek-r1:14b", stream=True):
    """调用生成文本接口"""
    url = "http://localhost:8000/generate"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "ap-czt-api"
    }
    
    data = {
        "model": model,
        "message": {
            "prompt": prompt,
            "system": system
        },
        "stream": stream,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "num_predict": -1,
        "stop": []
    }
    
    try:
        if stream:
            response = requests.post(url, headers=headers, json=data, stream=True)
            last_content = ""  # 用于存储上一次的内容
            for line in response.iter_lines():
                if line:
                    try:
                        line_str = line.decode('utf-8')
                        json_strings = line_str.split('}{')
                        for i, json_str in enumerate(json_strings):
                            if i > 0:
                                json_str = '{' + json_str
                            if i < len(json_strings) - 1:
                                json_str = json_str + '}'
                            
                            try:
                                chunk = json.loads(json_str)
                                if 'response' in chunk:
                                    content = chunk['response']  # 移除 strip()
                                    if not content:
                                        continue
                                    if content == '<think>':
                                        print('\n<think>\n', end='', flush=True)
                                    elif content == '</think>':
                                        print('\n</think>\n', end='', flush=True)
                                    else:
                                        # 检查是否需要添加空格
                                        if last_content and not last_content.endswith(' ') and not content.startswith(' '):
                                            print(' ', end='', flush=True)
                                        print(content, end='', flush=True)
                                        last_content = content
                                    time.sleep(0.05)
                            except json.JSONDecodeError:
                                continue
                    except Exception as e:
                        continue
            print()
            return {"success": True}
        else:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                return {
                    "success": False,
                    "error": f"请求失败: HTTP {response.status_code}",
                    "detail": response.text
                }
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_generate():
    """测试不同角色的生成能力"""
    test_cases = [
        {
            "role": "翻译专家",
            "system": "你是一位专业的中英互译专家，请准确翻译用户的输入",
            "prompt": "请将下面这句话翻译成英文：人工智能正在改变我们的生活方式"
        }
    ]
    
    for case in test_cases:
        print(f"\n=== {case['role']}测试 ===")
        print(f"系统提示: {case['system']}")
        print(f"用户提示: {case['prompt']}")
        print("\n生成结果:")
        
        response = generate_text(
            prompt=case['prompt'],
            system=case['system'],
            stream=True  # 默认使用流式输出
        )
        print("="*50)

if __name__ == "__main__":
    test_generate()