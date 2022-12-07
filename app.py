from pyChatGPT import ChatGPT
import gradio as gr
import os
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
    
def chat(message, history):
    history = history or []
    response = get_response_from_chatbot(message)
    history.append((message, response))
    return history, history

start_work = """async() => {
    function isMobile() {
        try {
            document.createEvent("TouchEvent"); return true;
        } catch(e) {
            return false; 
        }
    }
	function getClientHeight()
	{
	  var clientHeight=0;
	  if(document.body.clientHeight&&document.documentElement.clientHeight) {
		var clientHeight = (document.body.clientHeight<document.documentElement.clientHeight)?document.body.clientHeight:document.documentElement.clientHeight;
	  } else {
		var clientHeight = (document.body.clientHeight>document.documentElement.clientHeight)?document.body.clientHeight:document.documentElement.clientHeight;
	  }
	  return clientHeight;
	}
 
    function setNativeValue(element, value) {
      const valueSetter = Object.getOwnPropertyDescriptor(element.__proto__, 'value').set;
      const prototype = Object.getPrototypeOf(element);
      const prototypeValueSetter = Object.getOwnPropertyDescriptor(prototype, 'value').set;
      
      if (valueSetter && valueSetter !== prototypeValueSetter) {
            prototypeValueSetter.call(element, value);
      } else {
            valueSetter.call(element, value);
      }
    }
    var gradioEl = document.querySelector('body > gradio-app').shadowRoot;
    if (!gradioEl) {
        gradioEl = document.querySelector('body > gradio-app');
    }
    
    if (typeof window['gradioEl'] === 'undefined') {
        window['gradioEl'] = gradioEl;
        
        tabitems = window['gradioEl'].querySelectorAll('.tabitem');
        for (var i = 0; i < tabitems.length; i++) {    
            tabitems[i].childNodes[0].children[0].style.display='none';
            tabitems[i].childNodes[0].children[1].children[0].style.display='none';
            tabitems[i].childNodes[0].children[1].children[1].children[0].children[1].style.display="none"; 
        }    
        tab_demo = window['gradioEl'].querySelectorAll('#tab_demo')[0];
        tab_demo.style.display = "block";
        tab_demo.setAttribute('style', 'height: 100%;');
        const page1 = window['gradioEl'].querySelectorAll('#page_1')[0];
        const page2 = window['gradioEl'].querySelectorAll('#page_2')[0]; 
    
        page1.style.display = "none";
        page2.style.display = "block";    
    #     window['prevPrompt'] = '';
    #     window['doCheckPrompt'] = 0;
    #     window['checkPrompt'] = function checkPrompt() {
    #         try {
    #                 texts = window['gradioEl'].querySelectorAll('textarea');
    #                 text0 = texts[0];    
    #                 text1 = texts[1];
    #                 if (window['doCheckPrompt'] === 0 && window['prevPrompt'] !== text1.value) {
    #                         console.log('_____new prompt___[' + text1.value + ']_');
    #                         window['doCheckPrompt'] = 1;
    #                         window['prevPrompt'] = text1.value;
    #                         for (var i = 2; i < texts.length; i++) {
    #                             setNativeValue(texts[i], text1.value);
    #                             texts[i].dispatchEvent(new Event('input', { bubbles: true }));
    #                         }                        
    #                         setTimeout(function() {
    #                             btns = window['gradioEl'].querySelectorAll('button');
    #                             for (var i = 0; i < btns.length; i++) {
    #                                 if (btns[i].innerText == 'Submit') {
    #                                     btns[i].click();                
    #                                 }
    #                             }
    #                             window['doCheckPrompt'] = 0;
    #                         }, 10);                   
    #                 }
    #         } catch(e) {
    #         }        
    #     }
    #     window['checkPrompt_interval'] = window.setInterval("window.checkPrompt()", 100);         
    # }
   
    return false;
}"""

with gr.Blocks(title='Text to Image') as demo:
    with gr.Group(elem_id="page_1", visible=True) as page_1:
        with gr.Box():            
            with gr.Row():
                start_button = gr.Button("Let's GO!", elem_id="start-btn", visible=True) 
                start_button.click(fn=None, inputs=[], outputs=[], _js=start_work)

    with gr.Group(elem_id="page_2", visible=False) as page_2: 
        chatbot = gr.Chatbot(elem_id="chat_bot").style(color_map=("green", "gray"))
        chatbot.change(chat,
                    ["text", "state"],
                    [chatbot, "state"],
                    allow_flagging="never",
                    show_label=False,                       
                    show_progress=False)
        # chat_demo = gr.Interface(
        #     chat,
        #     ["text", "state"],
        #     [chatbot, "state"],
        #     allow_flagging="never",
        #     show_label=False,
        # )
        
# chatbot = gr.Chatbot().style(color_map=("green", "gray"))
# chatbot.change(show_progress=False)

# demo = gr.Interface(
#     chat,
#     ["text", "state"],
#     [chatbot, "state"],
#     allow_flagging="never",
#     show_label=False,
# )

demo.launch(debug = True)