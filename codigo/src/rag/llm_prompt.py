
from ollama import chat, Client, ResponseError # type: ignore
from src.rag.document_loader import load_documents

import requests
import json
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#todo: GET VARIABLES FROM config FILE
#https://github.com/ollama/ollama/blob/main/docs/api.md
#https://github.com/ollama/ollama-python
HOST = "http://localhost:11434/api/chat"
MODEL = "phi4-mini"
STREAM = False

def generate_diagram():
  logging.info("Carregando documentos de negócio")
  
  documents = load_documents()

  if not documents:
    raise "⚠️ The domain specific knowledge documents are missing"

  context_content = ""

  for filename, content in documents.items():
    logging.info(f"Getting domain specific knowledge from file: {filename} content:{content}")
    context_content += content
    logging.info(f"Domain specific knowledge loaded")

  logging.info("✅ {documents.size} Domain Specific Knowledge Files loaded.")

  sys_msg_content = f"""Act as a software architect specialized in modeling activity diagrams written in the PlantUML language
  with extensive experience in modeling systems for the hotel industry. Please always follow and made all 
  needed inferences using the specifications showed by the client: {content}"""

  usr_msg_content = """Please follow these steps to create a state machine diagram that presents all the states that need to be handled by the system you need to model:
  Step 1: Read and reason about the context information presented to you by the client of the system being modeled.
  Step 2: Identify all the states that a reservation can assume for all the possible possibilities within the reservation flow.
  Step 3: Now reason about the possible states and the restrictions presented by the client. Based on this, identify all the components (states, transitions, internal activities, internal transitions, self-transitions, choice pseudo-state, join, fork, composite states, input pseudo-state, output pseudo-state, join pseudo-state, sub-machine state, among others) that need to be specified to create a state machine diagram that supports all the possibilities presented in the reservation policy specifications.
  Step 4: Now write and return only the PlantUML code of the state machine diagram that represents all the reasoning capable of meeting all the constraints imposed by the customer on the reservation system."""

  sys_msg = mount_message("system",sys_msg_content)
  user_msg = mount_message("user",usr_msg_content)

  messages=[sys_msg,user_msg]

  call_ollama(messages)

def call_ollama(messages, host=HOST, model=MODEL):
  response = None
  
  try:
      logging.info(f"Calling Ollama API messages:{messages}, host:{host}, model:{model}")

      model_response = chat(model=MODEL, messages=messages, stream=STREAM)

      if model_response.done:
        logging.info(f"Result chat:{model_response.message.content}")
        response = model_response.message.content

  except ResponseError as e:
      logging.error('Error in get Ollama API call:', e.error)
          
  return response

def mount_message(role, content):
   return {
      'role': role,
      'content': content
    }