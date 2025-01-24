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

```py
from DuckDuckAI import ask

# Fetch response in streamed format (printing character by character)
ask("Tell me a joke", stream=True)

# Fetch response as a complete message
response = ask("Tell me a joke", stream=False)
print(response)

```

### Parameters Table

| Parameter | Type  | Description                                                         | Default       |
|-----------|-------|---------------------------------------------------------------------|---------------|
| query     | str   | The search query string.                                             | Required      |
| stream    | bool  | Whether to stream results or fetch them all at once.                 | True          |
| model     | str   | The model to use for the response (e.g., gpt-4o-mini).               | gpt-4o-mini   |

### List of Models

Here is the list of available models:

1. **mistralai/Mixtral-8x7B-Instruct-v0.1**: A model trained by Mistral for instruction-based tasks with 8x7B parameters.
2. **meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo**: Meta's large-scale model with 70 billion parameters designed for fast and accurate responses.
3. **claude-3-haiku-20240307**: A model optimized for generating short, poetic, and haiku-style text, using Claude 3 architecture.
4. **gpt-4o-mini**: A smaller variant of GPT-4 designed for quick, concise responses with less computation.


# License
This project is licensed under the Apache-2.0 license - see the LICENSE file for details.