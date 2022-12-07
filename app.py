from pyChatGPT import ChatGPT
import gradio as gr
import os, json
from loguru import logger
import random

session_token = os.environ.get('SessionToken')      
logger.info(f"session_token_: {session_token}")

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

def chat(message, chat_history):  
    out_chat = []
    if chat_history != '':
        out_chat = json.loads(chat_history)
    # print(f'chat_1_{chat_history}')
    response = get_response_from_chatbot(message)
    out_chat.append((message, response))
    chat_history = json.dumps(out_chat)
    # print(f'chat_2_{chat_history}')
    return out_chat, chat_history
    
with gr.Blocks(title='chat with chatgpt') as demo:
    with gr.Group(elem_id="page_1", visible=True) as page_1:
        with gr.Row(elem_id="prompt_row"):
            chatbot = gr.Chatbot(elem_id="chat_bot").style(color_map=("green", "blue"))
            chatbot1 = gr.Chatbot(elem_id="chat_bot1").style(color_map=("green", "blue"))
        with gr.Row():
            prompt_input0 = gr.Textbox(lines=1, label="prompt",show_label=False)
            chat_history = gr.Textbox(lines=4, label="prompt", visible=False)
            submit_btn = gr.Button(value = "submit",elem_id="submit-btn").style(
                    margin=True,
                    rounded=(True, True, True, True),
                    width=100
                )
            submit_btn.click(fn=chat, 
                             inputs=[prompt_input0, chat_history], 
                             outputs=[chatbot, chat_history],
                            )

demo.launch(debug = True)