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
    
# def chat(message, history):    
#     history = history or []
#     response = get_response_from_chatbot(message)
#     history.append((message, response))
#     return history, history

def chat1(message, chat_history):  
    split_mark_1 = ',,,,,,,,,,;'
    split_mark_2 = ';;;;;;;;;;;'
    out_chat = []
    if chat_history != '':
        ss0 = chat_history.split(split_mark_1)
        for ss1 in ss0:
            ss2 = ss1.split(split_mark_2)
            out_chat.append((ss2[0], ss2[1]))
    print(f'liuyz_1_{chat_history}')
    response = get_response_from_chatbot(message)
    out_chat.append((message, response))
    if chat_history != '':
        chat_history += split_mark_1
    chat_history += f'{message}{split_mark_2}{response}'
    print(f'liuyz_2_{chat_history}')
    return out_chat, chat_history

def chat(message, chat_history):  
    out_chat = []
    if chat_history != '':
        out_chat = json.loads(chat_history)
    print(f'liuyz_1_{chat_history}')
    response = get_response_from_chatbot(message)
    out_chat.append((message, response))
    # if chat_history != '':
    #     chat_history += split_mark_1
    # chat_history += f'{message}{split_mark_2}{response}'
    chat_history = json.dumps(out_chat)
    print(f'liuyz_2_{chat_history}')
    return out_chat, chat_history
    
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
    console.log('liuyz_1_')
    if (typeof window['gradioEl'] === 'undefined') {
        console.log('liuyz_2_')
        window['gradioEl'] = gradioEl;
        /*
        tabitems = window['gradioEl'].querySelectorAll('.tabitem');
        for (var i = 0; i < tabitems.length; i++) {    
            tabitems[i].childNodes[0].children[0].style.display='none';
            tabitems[i].childNodes[0].children[1].children[0].style.display='none';
            tabitems[i].childNodes[0].children[1].children[1].children[0].children[1].style.display="none"; 
        }    
        tab_demo = window['gradioEl'].querySelectorAll('#tab_demo')[0];
        tab_demo.style.display = "block";
        tab_demo.setAttribute('style', 'height: 100%;');
        */
        
        const page1 = window['gradioEl'].querySelectorAll('#page_1')[0];
        const page2 = window['gradioEl'].querySelectorAll('#page_2')[0]; 
        console.log('liuyz_3_')
        page1.style.display = "none";
        page2.style.display = "block";    
        console.log('liuyz_4_')

        /*
        window['prevPrompt'] = '';
        window['doCheckPrompt'] = 0;
        window['checkPrompt'] = function checkPrompt() {
            try {
                    texts = window['gradioEl'].querySelectorAll('textarea');
                    text0 = texts[0];    
                    text1 = texts[1];
                    if (window['doCheckPrompt'] === 0 && window['prevPrompt'] !== text1.value) {
                            console.log('_____new prompt___[' + text1.value + ']_');
                            window['doCheckPrompt'] = 1;
                            window['prevPrompt'] = text1.value;
                            for (var i = 2; i < texts.length; i++) {
                                setNativeValue(texts[i], text1.value);
                                texts[i].dispatchEvent(new Event('input', { bubbles: true }));
                            }                        
                            setTimeout(function() {
                                btns = window['gradioEl'].querySelectorAll('button');
                                for (var i = 0; i < btns.length; i++) {
                                    if (btns[i].innerText == 'Submit') {
                                        btns[i].click();                
                                    }
                                }
                                window['doCheckPrompt'] = 0;
                            }, 10);                   
                    }
            } catch(e) {
            }        
        }
        window['checkPrompt_interval'] = window.setInterval("window.checkPrompt()", 100);  
        */
    }
   
    return false;
}"""

with gr.Blocks(title='Text to Image') as demo:
    with gr.Group(elem_id="page_1", visible=True) as page_1:
    #     with gr.Box():            
    #         with gr.Row():
    #             start_button = gr.Button("Let's GO!", elem_id="start-btn", visible=True) 
    #             start_button.click(fn=None, inputs=[], outputs=[], _js=start_work)

    # with gr.Group(elem_id="page_2", visible=False) as page_2: 
            with gr.Row(elem_id="prompt_row"):
                chatbot = gr.Chatbot(elem_id="chat_bot").style(color_map=("green", "gray"))   
            with gr.Row():
                prompt_input0 = gr.Textbox(lines=1, label="prompt",show_label=False)
                chat_history = gr.Textbox(lines=4, label="prompt", visible=True)
                submit_btn = gr.Button(value = "submit",elem_id="submit-btn").style(
                        margin=True,
                        rounded=(True, True, True, True),
                        width=100
                    )
                submit_btn.click(fn=chat, 
                                 inputs=[prompt_input0, chat_history], 
                                 outputs=[chatbot, chat_history],
                                )
                
        # chatbot = gr.Chatbot(elem_id="chat_bot").style(color_map=("green", "gray"))
        # prompt_input0 = gr.Textbox(lines=4, label="prompt")
        # chatbot.change(chat,
        #             ["text", "state"],
        #             [chatbot, "state"],
        #             allow_flagging="never",
        #             show_label=False,                       
        #             show_progress=False)
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