from pyChatGPT import ChatGPT
import gradio as gr
import os
from loguru import logger
import random

session_token = os.environ.get('SessionToken')      
logger.info(f"session_token_: {session_token}")

# def chat(text):
#     try:
#       api = ChatGPT(session_token) 
#       resp = api.send_message(text)    
#       api.refresh_auth() 
#       api.reset_conversation() 
#       response = resp['message']
#       logger.info(f"response_: {response}")
#     except:
#       response = "Sorry, I'm am tired."
#     return response


# demo = gr.Interface(chat,
#               inputs = [gr.Textbox(label = 'Input： ')], 
#                outputs = gr.outputs.Textbox(type="text",label="from ChatGPT："), 
#                title = "Talk with ChatGPT",
#                description= "")

def get_response_from_chatbot(text):
    try:
      api = ChatGPT(session_token) 
      resp = api.send_message(text)    
      api.refresh_auth() 
      api.reset_conversation() 
      response = resp['message']
      logger.info(f"response_: {response}")
    except:
      response = "Sorry, I'm am tired."
    return response
    
def chat(message, history):
    history = history or []
    response = get_response_from_chatbot(message)
    # message = message.lower()
    # if message.startswith("how many"):
    #     response = random.randint(1, 10)
    # elif message.startswith("how"):
    #     response = random.choice(["Great", "Good", "Okay", "Bad"])
    # elif message.startswith("where"):
    #     response = random.choice(["Here", "There", "Somewhere"])
    # else:
    #     response = "I don't know"
    history.append((message, response))
    return history, history

chatbot = gr.Chatbot().style(color_map=("green", "pink"))
demo = gr.Interface(
    chat,
    ["text", "state"],
    [chatbot, "state"],
    allow_flagging="never",
)

demo.launch(debug = True)