// 添加在文件开头
function loadScriptWithAuth(script) {
    fetch(script.src, {
        headers: {
            'X-API-Key': 'ap-czt-api'
        }
    })
    .then(response => response.text())
    .then(js => {
        const newScript = document.createElement('script');
        newScript.textContent = js;
        document.body.appendChild(newScript);
    });
}

// 移除固定的 API_KEY
// const API_KEY = 'ap-czt-api';

let currentService = 'chat';
let chatHistory = [];

function switchService(service) {
    currentService = service;
    document.getElementById('chatBtn').classList.toggle('active', service === 'chat');
    document.getElementById('generateBtn').classList.toggle('active', service === 'generate');
    document.getElementById('systemPrompt').style.display = service === 'generate' ? 'block' : 'none';
    document.getElementById('messages').innerHTML = '';
    chatHistory = [];
}

async function sendMessage() {
    const input = document.getElementById('userInput');
    const messages = document.getElementById('messages');
    const modelSelect = document.getElementById('modelSelect');
    const streamingToggle = document.getElementById('streamingToggle');
    const apiKey = document.getElementById('apiKeyInput').value;
    
    const userMessage = input.value.trim();
    if (!userMessage) return;
    
    // 添加用户消息
    const userDiv = document.createElement('div');
    userDiv.className = 'message user-message';
    userDiv.textContent = userMessage;
    messages.appendChild(userDiv);
    
    // 清空输入框
    input.value = '';
    
    // 添加助手消息容器
    const assistantDiv = document.createElement('div');
    assistantDiv.className = 'message assistant-message';
    messages.appendChild(assistantDiv);
    
    try {
        const endpoint = currentService === 'chat' ? '/chat' : '/generate';
        let requestBody;
        
        if (currentService === 'chat') {
            // 添加用户消息到历史记录
            chatHistory.push({ role: 'user', content: userMessage });
            
            requestBody = {
                model: modelSelect.value,
                messages: chatHistory,
                stream: streamingToggle.checked,
                temperature: 0.7,
                top_p: 0.9,
                top_k: 40
            };
        } else {
            requestBody = {
                model: modelSelect.value,
                message: {
                    prompt: userMessage,
                    system: document.getElementById('systemInput')?.value || null
                },
                stream: streamingToggle.checked,
                temperature: 0.7,
                top_p: 0.9,
                top_k: 40
            };
        }

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': apiKey
            },
            body: JSON.stringify(requestBody)
        });

        let assistantMessage = '';

        if (streamingToggle.checked) {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            while (true) {
                const {value, done} = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');
                
                for (const line of lines) {
                    if (line.trim()) {
                        try {
                            const data = JSON.parse(line);
                            let content = '';
                            if (currentService === 'chat' && data.message?.content) {
                                content = data.message.content;
                            } else if (data.response) {
                                content = data.response;
                            }
                            
                            if (content) {
                                if (content === '<think>') {
                                    assistantMessage += '\n<think>\n';
                                } else if (content === '</think>') {
                                    assistantMessage += '\n</think>\n';
                                } else {
                                    assistantMessage += content;
                                }
                                // 使用 innerHTML 来保持换行格式
                                assistantDiv.innerHTML = assistantMessage
                                    .replace(/\n<think>\n/g, '<div class="think-tag">&lt;think&gt;</div>')
                                    .replace(/\n<\/think>\n/g, '<div class="think-tag">&lt;/think&gt;</div>');
                            }
                        } catch (e) {
                            console.error('解析错误:', e);
                        }
                    }
                }
            }
        } else {
            const data = await response.json();
            if (currentService === 'chat') {
                assistantMessage = data.message?.content || '';
            } else {
                assistantMessage = data.response || '';
            }
            assistantDiv.textContent = assistantMessage;
        }

        // 添加助手回复到历史记录
        if (currentService === 'chat') {
            chatHistory.push({ role: 'assistant', content: assistantMessage });
        }
    } catch (error) {
        assistantDiv.textContent = `错误: ${error.message}`;
    }
    
    // 滚动到底部
    messages.scrollTop = messages.scrollHeight;
}

// 支持按回车发送
document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// 初始化
switchService('chat');