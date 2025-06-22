import requests
import json

def summarize_text_llama3(text):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "llama3",
        "messages": [
            {"role": "user", "content": f"Summarize the following text:\n{text}"}
        ],
        "stream": True
    }

    response = requests.post(url, json=payload, stream=True)

    full_response = ""
    for line in response.iter_lines():
        if line:
            try:
                chunk = line.decode("utf-8")
                data = json.loads(chunk) if chunk.startswith("{") else {}
                content = data.get("message", {}).get("content")
                if content:
                    full_response += content
            except Exception as e:
                print("Chunk parse error:", e)
    
    return full_response

