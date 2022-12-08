from pyChatGPT import ChatGPT
import gradio as gr
import os, json
from loguru import logger
import random

session_token = os.environ.get('SessionToken')      
# logger.info(f"session_token_: {session_token}")

def get_response_from_chatbot(text):
    try:
      api = ChatGPT(session_token) 
      resp = api.send_message(text)    
      api.refresh_auth() 
      api.reset_conversation() 
      response = resp['message']
      # logger.info(f"response_: {response}")
    except:
      response = "Sorry, I'm tired."
    return response

def chat(message, chat_history):      
    out_chat = []
    if chat_history != '':
        out_chat = json.loads(chat_history)
    response = get_response_from_chatbot(message)
    out_chat.append((message, response))
    chat_history = json.dumps(out_chat)
    logger.info(f"out_chat_: {len(out_chat)}")
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
    
    if (typeof window['gradioEl'] === 'undefined') {
        window['gradioEl'] = gradioEl;
       
        const page1 = window['gradioEl'].querySelectorAll('#page_1')[0];
        const page2 = window['gradioEl'].querySelectorAll('#page_2')[0]; 
    
        page1.style.display = "none";
        page2.style.display = "block";

        window['div_count'] = 0;
        window['chat_bot'] = window['gradioEl'].querySelectorAll('#chat_bot')[0];
        window['chat_bot1'] = window['gradioEl'].querySelectorAll('#chat_bot1')[0];   
        chat_row = window['gradioEl'].querySelectorAll('#chat_row')[0]; 
        prompt_row = window['gradioEl'].querySelectorAll('#prompt_row')[0]; 
        window['chat_bot1'].children[1].textContent = '';
        
        clientHeight = getClientHeight();
        if (isMobile()) {
            window['gradioEl'].querySelectorAll('#component-1')[0].style.display = "none";
            window['gradioEl'].querySelectorAll('#component-2')[0].style.display = "none";
            new_height = (clientHeight - 200) + 'px';
        } else {
            new_height = (clientHeight - 300) + 'px';
        }
        chat_row.style.height = new_height;
        window['chat_bot'].style.height = new_height;
        window['chat_bot'].children[2].style.height = new_height;
        window['chat_bot1'].style.height = new_height;
        window['chat_bot1'].children[2].style.height = new_height;
        prompt_row.children[0].style.flex = 'auto';
        prompt_row.children[0].style.width = '100%';
        prompt_row.children[0].setAttribute('style','flex-direction: inherit; flex: 1 1 auto; width: 100%;border-color: green;')
                
        window['checkChange'] = function checkChange() {
            try {
                if (window['chat_bot'].children[2].children[0].children.length > window['div_count']) {
                    new_len = window['chat_bot'].children[2].children[0].children.length - window['div_count'];
                    for (var i = 0; i < new_len; i++) { 
                        new_div = window['chat_bot'].children[2].children[0].children[window['div_count'] + i].cloneNode(true);
                        window['chat_bot1'].children[2].children[0].appendChild(new_div);
                    }
                    window['div_count'] = chat_bot.children[2].children[0].children.length;
                }
                if (window['chat_bot'].children[0].children.length > 1) {
                     window['chat_bot1'].children[1].textContent = window['chat_bot'].children[0].children[1].textContent;
                } else {
                    window['chat_bot1'].children[1].textContent = '';
                }
              
            } catch(e) {
            }        
        }
        window['checkChange_interval'] = window.setInterval("window.checkChange()", 500);         
    }
   
    return false;
}"""


with gr.Blocks(title='Talk to chatGPT') as demo:
    gr.HTML("<p>You can duplicating this space and use your own session token: <a style='display:inline-block' href='https://huggingface.co/spaces/yizhangliu/chatGPT?duplicate=true'><img src='https://img.shields.io/badge/-Duplicate%20Space-blue?labelColor=white&style=flat&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAP5JREFUOE+lk7FqAkEURY+ltunEgFXS2sZGIbXfEPdLlnxJyDdYB62sbbUKpLbVNhyYFzbrrA74YJlh9r079973psed0cvUD4A+4HoCjsA85X0Dfn/RBLBgBDxnQPfAEJgBY+A9gALA4tcbamSzS4xq4FOQAJgCDwV2CPKV8tZAJcAjMMkUe1vX+U+SMhfAJEHasQIWmXNN3abzDwHUrgcRGmYcgKe0bxrblHEB4E/pndMazNpSZGcsZdBlYJcEL9Afo75molJyM2FxmPgmgPqlWNLGfwZGG6UiyEvLzHYDmoPkDDiNm9JR9uboiONcBXrpY1qmgs21x1QwyZcpvxt9NS09PlsPAAAAAElFTkSuQmCC&logoWidth=14' alt='Duplicate Space'></a></p>")
    gr.HTML("<p> Instruction on how to get session token can be seen in video <a style='display:inline-block' href='https://www.youtube.com/watch?v=TdNSj_qgdFk'><font style='color:blue;weight:bold;'>here</font></a>. Add your session token by going to settings and add under secrets. </p>")
    with gr.Group(elem_id="page_1", visible=True) as page_1:
        with gr.Box():            
            with gr.Row():
                start_button = gr.Button("Let's talk to chatGPT!", elem_id="start-btn", visible=True) 
                start_button.click(fn=None, inputs=[], outputs=[], _js=start_work)
                
    with gr.Group(elem_id="page_2", visible=False) as page_2:        
        with gr.Row(elem_id="chat_row"):
            chatbot = gr.Chatbot(elem_id="chat_bot", visible=False).style(color_map=("green", "blue"))
            chatbot1 = gr.Chatbot(elem_id="chat_bot1").style(color_map=("green", "blue"))
        with gr.Row(elem_id="prompt_row"):
            prompt_input = gr.Textbox(lines=2, label="prompt",show_label=False)
            chat_history = gr.Textbox(lines=4, label="prompt", visible=False)
            submit_btn = gr.Button(value = "submit",elem_id="submit-btn").style(
                    margin=True,
                    rounded=(True, True, True, True),
                    width=100
                )
            submit_btn.click(fn=chat, 
                             inputs=[prompt_input, chat_history], 
                             outputs=[chatbot, chat_history],
                            )

demo.launch(debug = True)