# DuckDuckAI

DuckDuckAI is a Python package for interacting with DuckDuckGo's chat API. It allows you to fetch responses from DuckDuckGo's AI models and print them in a streamed format or as a complete response.

## Installation

To install the DuckDuckAI package, you can use pip:

```bash
pip install DuckDuckAI
```

## Usage

You can interact with DuckDuckAI by calling the `ask` function. It supports both streaming responses or returning the entire message at once.

### Example

```python
from duckduckai import ask

# Fetch response in streamed format (printing character by character)
ask("Tell me a joke", stream=True)[0] # Use 0 if you want to retrieve it inside a variable.

# Fetch response as a complete message
response = ask("Tell me a joke", stream=False)
print(response)
```

### Parameters

| Parameter | Type  | Description                                                         | Default       |
|-----------|-------|---------------------------------------------------------------------|---------------|
| query     | str   | The search query string.                                             | Required      |
| stream    | bool  | Whether to stream results or fetch them all at once.                 | True          |
| model     | str   | The model to use for the response.                                   | gpt-4o-mini   |

## Available Models

DuckDuckAI currently supports the following models:

| Model ID | Description |
|----------|-------------|
| `gpt-4o-mini` | A smaller variant of GPT-4o designed for quick, concise responses with less computation. |
| `meta-llama/Llama-3.3-70B-Instruct-Turbo` | Meta's large-scale Llama 3.3 model with 70 billion parameters designed for fast and accurate responses. |
| `claude-3-haiku-20240307` | Anthropic's Claude 3 Haiku model optimized for efficient, high-quality responses. |
| `mistralai/Mistral-Small-24B-Instruct-2501` | Mistral AI's 24 billion parameter model trained for instruction-based tasks. |
| `o3-mini` | OpenAI's compact reasoning model optimized for lightweight performance. |

Additional models may be available but subject to access restrictions. Some models may require specific permissions or may not be available in all regions.

## Advanced Usage

You can reuse the authentication token to make multiple requests more efficiently:

```python
from duckduckai import ask, fetch_x_vqd_token

# Fetch a token once
token = fetch_x_vqd_token()

# Use the same token for multiple requests
response1 = ask("What is quantum computing?", model="gpt-4o-mini", token=token)[0]  # Do not put [0] if you want the token in the response
response2 = ask("Explain neural networks", model="claude-3-haiku-20240307", token=token)[0] # Do not put [0] if you want the token in the response
```

## License

This project is licensed under the Apache-2.0 license - see the LICENSE file for details.
