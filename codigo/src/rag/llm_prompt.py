import ollama
from ollama import Client

import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#https://github.com/ollama/ollama/blob/main/docs/api.md
#https://github.com/ollama/ollama-python
host = "http://localhost:11434/api/chat"
model = "phi4-mini"
stream = False

messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
]

try:
    response = ollama.chat(model=model, messages=messages, stream=stream)
    if response.done:
        logging.info(f"Result chat:{response.message.content}")

except ollama.ResponseError as e:
    logging.error('Error in Ollama API call:', e.error)