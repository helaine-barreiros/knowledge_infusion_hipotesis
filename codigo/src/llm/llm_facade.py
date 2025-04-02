import requests
import json
import logging
import os

from dotenv import load_dotenv
from ollama import chat, Client, ResponseError
from openai import OpenAI
from utils.system_parametrization import SYSTEM_CONFIG
from utils.document_loader import load_documents
from llm.document_loader import load_documents
from utils.logger import Logger

from openai.types.beta.threads.message_create_params import (
    Attachment,
    AttachmentToolFileSearch,
)

logging = Logger
load_dotenv() 

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_CLIENT = OpenAI(api_key=OPENAI_KEY)
OPENAI_MODEL = SYSTEM_CONFIG.get("openai_model")

SYS_MSG_CONTENT = SYSTEM_CONFIG.get("system_prompt")
USR_MSG_CONTENT = SYSTEM_CONFIG.get("user_prompt")

OLLAMA_HOST = SYSTEM_CONFIG.get("ollama_url")
OLLAMA_MODEL = SYSTEM_CONFIG.get("ollama_model")

DSK_DIRECTORY = SYSTEM_CONFIG.get("dsk_dir")

def generate_diagram(output_directory, filename, llm="Ollama", use_specific_knowledge=False):
  logging.info("Starting diagram generation")

  filenames = None
  domain_knowledge_context_content = None
  usr_msg_content = USR_MSG_CONTENT
  sys_msg_content = SYS_MSG_CONTENT

  if use_specific_knowledge:
    logging.info("Using domain-specific knowledge for diagram generation")

    if llm == "Ollama":
      #fixme: adjust do pdf document upload, mut use only text for now!!!!!
      domain_knowledge_context_content = get_domain_knowledge_content_to_ollama()
      usr_msg_content = f"""{usr_msg_content} Use this Business constraints to generate the diagram: {domain_knowledge_context_content}"""
    else:
      #filenames, domain_knowledge_context_content = get_domain_knowledge_content_to_openai()
      filenames = atach_domain_knowledge_files_to_openai
      usr_msg_content = f"""{usr_msg_content}. To generate the diagram use the Business Domain Knowledge in the attached files: {", ".join(filenames)}"""

    logging.info("Domain-specific knowledge successfully loaded")

  else:
    logging.info("Generating diagram without domain-specific knowledge")

  plantuml_code = ""

  try:
    if llm == "Ollama":
      sys_msg = mount_message("system",sys_msg_content)
      user_msg = mount_message("user",usr_msg_content)

      messages=[sys_msg,user_msg]

      plantuml_code = call_ollama(messages)
    else:
      plantuml_code = call_openai(instructions=sys_msg_content, input=usr_msg_content, file_ids=filenames)

  except Exception as e:
    logging.critical(f"Failed to generate diagram using {llm}: {e}")
    raise ValueError(f"Failed to generate diagram using {llm}: {e}") from e

  logging.info("Diagram successfully generated:{plantuml_code}")

  output_file = os.path.join(output_directory, f"{filename}.txt")

  try:
    with open(output_file, 'w', encoding='utf-8') as file:
      file.write(plantuml_code)

    logging.info(f"LLM response saved successfully at: {output_file}")
  except Exception as e:
    logging.critical(f"Failed to save LLM response at {output_file}: {e}")
    raise Exception(f"Failed to save LLM response at {output_file}: {e}")

  return plantuml_code

def get_domain_knowledge_content_to_openai():
  content = []

  try:
      domain_knowledge_documents = load_documents(load_pdf_in_base64=True)
  except Exception as e:
      logging.critical(f"Failed to load domain-specific documents to OpenAI: {e}")
      raise Exception(f"Failed to load domain-specific documents to OpenAI: {e}")

  if not domain_knowledge_documents:
    logging.error("No domain-specific documents found. Cannot proceed with diagram generation.")
    raise Exception("The diagram generation requires domain-specific knowledge, but no documents were found.")
  
  for filename, file_content in domain_knowledge_documents.items():
    content.append({
      "type": "input_file",
      "filename": filename,
      "file_data": file_content
    })
    
  return domain_knowledge_documents.keys, content

def get_domain_knowledge_content_to_ollama():
  domain_knowledge_context_content = ""
  logging.info("Using domain-specific knowledge for OLLAMA to diagram generation")
  
  domain_knowledge_documents = None

  try:
      domain_knowledge_documents = load_documents()
  except Exception as e:
      logging.critical(f"Failed to load domain-specific documents: {e}")
      raise Exception(f"Failed to load domain-specific documents: {e}")

  if not domain_knowledge_documents:
    logging.error("No domain-specific documents found. Cannot proceed with diagram generation.")
    raise Exception("The diagram generation requires domain-specific knowledge, but no documents were found.")

  for filename, content in domain_knowledge_documents.items():
    logging.debug(f"Processing domain knowledge file: {filename}")
    domain_knowledge_context_content += content

  return domain_knowledge_context_content

def call_ollama(messages):
  response = None

  if not OLLAMA_HOST:
    logging.critical("OLLAMA URL is not configured in .yaml or provided as a parameter.")
    raise ValueError("OLLAMA URL is required but not found.")

  if not OLLAMA_MODEL:
    logging.critical("OLLAMA Model is not configured in .yaml or provided as a parameter.")
    raise ValueError("OLLAMA Model is required but not found.")

  if not messages:
    logging.debug("The OLLAMA call messages are not provided.")
    raise ValueError("The OLLAMA call messages are not provided.")

  logging.info(f"Initiating Ollama API call | Host: {host} | Model: {model}")
  logging.debug(f"Request Messages: {messages}")

  try:
      model_response = chat(model=OLLAMA_MODEL, messages=messages, stream=False)

      if model_response.done:
        response = model_response.message.content
        logging.info("Ollama API call successful.")
        logging.debug(f"Response Content: {response}")
      else:
        logging.warning("Ollama API call completed but response not marked as 'done'.")

  except ResponseError as e:
      logging.error(f"Ollama API error: {e.error}")
  except Exception as e:
        logging.critical(f"Unexpected error in Ollama API call: {e}")

  return response

def call_openai(instructions, input, file_ids):
    response = None
    
    if not instructions or not input:
      logging.debug("The OPENAI call messages are not provided.")
      raise ValueError("The OPENAI call messages are not provided.")

    if not OPENAI_KEY:
      logging.critical("OpenAI API Key is not configured in .env or provided as a parameter.")
      raise ValueError("OpenAI API Key is required but not found.")

    if not OPENAI_MODEL:
      logging.critical("OpenAI Model is not configured in .yaml or provided as a parameter.")
      raise ValueError("OpenAI Model is required but not found.")

    try:

      logging.info("Initializing OpenAI client.")        
      logging.info(f"Calling OpenAI API | Model: {model}")
      logging.debug(f"Instructions: {instructions}")
      logging.debug(f"User Input: {input}")

      file_assistant = OPENAI_CLIENT.beta.assistants.create(
          model=OPENAI_MODEL,
          description="An assistant to generate UML Diagrams.",
          tools=[{"type": "file_search"}],
          name="File assistant",
      )

      thread = OPENAI_CLIENT.beta.threads.create()

      OPENAI_CLIENT.beta.threads.messages.create(
        thread_id=thread.id,
        messages=[
          {"role": "developer", "content": instructions},
          {"role": "user", "content": input, },
        ]
        role="user",
        ,
        content=prompt,
      )




      messages = [
          {"role": "developer", "content": instructions},
          {"role": "user", "content": input},  
      ]

      kwargs = {"file_ids": file_ids} if file_ids else {}
      
      response_result = OPENAI_CLIENT.chat.completions.create(
          model=OPENAI_MODEL,
          messages=messages,
          **kwargs
      )
      
      if response_result.choices:
        response = response_result.choices[0].message.content
        logging.info("OpenAI API call successful.")
        logging.debug(f"Response Content: {response}")
      else:
        logging.warning("OpenAI API call returned an empty response.")

    except Exception as e:
        logging.error(f"Error in OpenAI API call: {str(e)}")

    return response

def atach_domain_knowledge_files_to_openai():
  files = []

  if not DSK_DIRECTORY:
    logging.critical("Could not send Domain Knowledg Files in OpenAI. Configuration error: 'dsk_dir' is missing in CONFIG")
    raise Exception("Could not send Domain Knowledg Files in OpenAI. Configuration error: 'dsk_dir' is missing in CONFIG")
   
  try:
      files = [f for f in os.listdir(DSK_DIRECTORY) if os.path.isfile(os.path.join(DSK_DIRECTORY, f))]

      sended_files = {}

      for file in files:
        file_path = os.path.join(DSK_DIRECTORY, file)

        with open(file_path, "rb") as f:
            uploaded_file = OPENAI_CLIENT.files.create(file=f, purpose="assistants")
            sended_files[uploaded_file.id] = file

      file_ids = list(sended_files.keys())

  except Exception as e:
      logging.critical(f"Failed to send domain-specific documents to OpenAI: {e}")
      raise Exception(f"Failed to send domain-specific documents to OpenAI: {e}")
  
  return file_ids
  
    
def mount_message(role, content):
   return {
      'role': role,
      'content': content
    }
