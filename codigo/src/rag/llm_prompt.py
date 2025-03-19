
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

  #logging.info(f"✅ {documents.size} Domain Specific Knowledge Files loaded.")

  sys_msg_content = f"""You are a software architect specialized in UML modeling, particularly state diagrams implemented in PlantUML. Your role is to create precise and complete diagrams based on business requirements. Return ONLY valid PlantUML code, starting with @startuml and ending with @enduml, without additional explanations or comments in the code."""

  usr_msg_content = f"""Model a UML 'State Diagram' in PlantUML Language for a hotel reservation system that should represent the complete lifecycle of a reservation.
The diagram should capture all possible states of a reservation (such as Requested, Confirmed, Canceled, Completed) and the permitted transitions between these states.
Return ONLY the PlantUML code between the @startuml and @enduml tags, without explanations or additional text.

Use this example to remember the PlantUML language syntax:
@startuml
state start1 <<start>>
state choice1 <<choice>>
state fork1 <<fork>>
state join2 <<join>>
state end3 <<end>>
[*] --> choice1 : from start\nto choice
start1 --> choice1 : from start stereo\nto choice
choice1 --> fork1 : from choice\nto fork
choice1 --> join2 : from choice\nto join
choice1 --> end3 : from choice\nto end stereo
fork1 ---> State1 : from fork\nto state
fork1 --> State2 : from fork\nto state
State2 --> join2 : from state\nto join
State1 --> [*] : from state\nto end
join2 --> [*] : from join\nto end
@enduml

Business constraints to consider:
{context_content}"""

  sys_msg = mount_message("system",sys_msg_content)
  user_msg = mount_message("user",usr_msg_content)

  messages=[sys_msg,user_msg]

  plantuml_code = call_ollama(messages)
  logging.info(f"PlantUML CODE: {plantuml_code}")

  return plantuml_code

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
