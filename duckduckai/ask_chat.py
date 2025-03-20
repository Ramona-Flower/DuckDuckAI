import requests
import json

def fetch_x_vqd_token():
    """
    Fetches the X-Vqd-4 token from DuckDuckGo status endpoint.
    Returns:
        tuple: (X-Vqd-4 token, X-Vqd-Hash-1 token) if found, (None, None) otherwise.
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
    response = requests.get(status_url, headers=headers)
    
    if response.status_code != 200:
        return None, None
    
    x_vqd_4 = response.headers.get("X-Vqd-4")
    x_vqd_hash_1 = response.headers.get("x-vqd-hash-1")
    
    return x_vqd_4, x_vqd_hash_1

def ask(query, stream=True, model="gpt-4o-mini", token=None, token_hash=None):
    """
    Fetches the response from DuckDuckGo's chat API.
    
    Args:
        query (str): The query to send to the API.
        stream (bool): Whether to stream the response (True) or fetch it all at once (False).
        model (str): The model to use for the query (default is "gpt-4o-mini").
        token (str, optional): A manually provided X-Vqd-4 token. If None, a new token will be fetched.
        token_hash (str, optional): A manually provided X-Vqd-Hash-1 token. If None, a new token hash will be fetched.
    
    Returns:
        tuple: (result, token, token_hash) where result is the full message if not streamed or None if streamed,
               and token/token_hash are the X-Vqd-4 and X-Vqd-Hash-1 tokens used (can be reused in future calls).
    """
    if not token or not token_hash:
        token, token_hash = fetch_x_vqd_token()
        if not token:
            return "Failed to fetch token", None, None
    
    chat_url = "https://duckduckgo.com/duckchat/v1/chat"
    chat_headers = {
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "Referer": "https://duckduckgo.com/",
        "Origin": "https://duckduckgo.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "X-Vqd-4": token,
        "x-vqd-hash-1": token_hash,
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
    
    if response.status_code == 401:
        new_token, new_token_hash = fetch_x_vqd_token()
        if new_token:
            return ask(query, stream, model, new_token, new_token_hash)
        else:
            return "Failed to fetch new token after 401 error", None, None
    
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
        return full_message, token, token_hash
    return None, token, token_hash
