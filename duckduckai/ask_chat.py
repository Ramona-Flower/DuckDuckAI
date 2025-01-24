import requests
import json

def fetch_x_vqd_token():
    """
    Fetches the X-Vqd-4 token from DuckDuckGo status endpoint.

    Returns:
        str: The X-Vqd-4 token if found, None otherwise.
    """
    status_url = "https://duckduckgo.com/duckchat/v1/status"
    headers = {
        "Accept": "*/*",
        "Referer": "https://duckduckgo.com/",
        "Origin": "https://duckduckgo.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Dnt": "1",
        "Sec-Gpc": "1",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Priority": "u=1, i",
        "X-Vqd-Accept": "1",
    }

    status_response = requests.get(status_url, headers=headers)
    if status_response.status_code != 200:
        return None  

    x_vqd_4 = status_response.headers.get("X-Vqd-4")
    if not x_vqd_4:
        return None 

    return x_vqd_4


def ask(query, stream=True, model="gpt-4o-mini"):
    """
    Fetches the response from DuckDuckGo's chat API and processes it.

    Args:
        query (str): The query to send to the API.
        stream (bool): Whether to stream the response (True) or fetch it all at once (False).
        model (str): The model to use for the query (default is "gpt-4o-mini").

    Returns:
        str or None: The full message if not streamed, or None if streamed.
    """
    x_vqd_4 = fetch_x_vqd_token()
    if not x_vqd_4:
        return "Failed to fetch token" 

    chat_url = "https://duckduckgo.com/duckchat/v1/chat"
    chat_headers = {
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "Referer": "https://duckduckgo.com/",
        "Origin": "https://duckduckgo.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "X-Vqd-4": x_vqd_4,
        "Dnt": "1",
        "Sec-Gpc": "1",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Priority": "u=1, i",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": query}]
    }
    response = requests.post(chat_url, headers=chat_headers, json=payload, stream=True)

    full_message = ""
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith("data:"):
                try:
                    data = decoded_line[len("data: "):]
                    json_data = json.loads(data)
                    if "message" in json_data:
                        if stream:
                            for char in json_data["message"]:
                                print(char, end="", flush=True)
                        else:
                            full_message += json_data["message"]
                except json.JSONDecodeError:
                    pass  

    if not stream:
        return full_message

    return None  
