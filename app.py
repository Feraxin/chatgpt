from pyChatGPT import ChatGPT
import os
from loguru import logger

def chat(text):
    try:
      session_token = os.environ.get('SessionToken')      
      logger.info(f"session_token_: {session_token}")
      api = ChatGPT(session_token) 
      resp = api.send_message(text)    
      api.refresh_auth() 
      api.reset_conversation() 
      response = resp['message']
      logger.info(f"response_: {response}")
    except:
      response = "Sorry, I'm am tired."
    return response

import gradio as gr
demo = gr.Interface(chat,
              inputs = [gr.Textbox(label = 'Input： ')], 
               outputs = gr.outputs.Textbox(type="text",label="from ChatGPT："), 
               title = "talk with ChatGPT",
               description= "")
demo.launch(debug = True)