import requests
import json


def stream_ai_response(user_prompt, system_prompt="You are a super smart helpful assistant"):
    r = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.2",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": True,
        },
        timeout=120,
        stream=True
    )

    try:
        r.raise_for_status()
        for line in r.iter_lines():
            if line:
                chunk = json.loads(line)
                if "message" in chunk and "content" in chunk["message"]:
                    content = chunk["message"]["content"]
                    yield content
                if chunk.get("done", False):
                    break
    except Exception as e:
        yield f"Error: {e}"

