from pyChatGPT import ChatGPT
import gradio as gr
import os, sys, json
from loguru import logger
import paddlehub as hub
import random

language_translation_model = hub.Module(directory=f'./baidu_translate')
def getTextTrans(text, source='zh', target='en'):
    try:
        text_translation = language_translation_model.translate(text, source, target)
        return text_translation
    except Exception as e:
        return text 

session_token = os.environ.get('SessionToken')      
# logger.info(f"session_token_: {session_token}")

def get_api():
    try:
      api = ChatGPT(session_token)
      api.refresh_auth()
    except:
      api = None
    return api
    
def get_response_from_chatbot(api, text):
    if api is None:
        return "Sorry, I'm busy. Try again later.(1)"
    try:
      resp = api.send_message(text)    
      api.refresh_auth()
      # api.reset_conversation() 
      response = resp['message']
      conversation_id = resp['conversation_id']
      parent_id = resp['parent_id']
      # logger.info(f"response_: {response}")
      logger.info(f"conversation_id_: [{conversation_id}] / parent_id: [{parent_id}]")  
    except:
      response = "Sorry, I'm busy. Try again later.(2)"
    return response

model_ids = {
            # "models/stabilityai/stable-diffusion-2-1":"sd-v2-1",
            # "models/stabilityai/stable-diffusion-2":"sd-v2-0",
            # "models/runwayml/stable-diffusion-v1-5":"sd-v1-5",
            # "models/CompVis/stable-diffusion-v1-4":"sd-v1-4",
            "models/prompthero/openjourney":"openjourney",
            # "models/ShadoWxShinigamI/Midjourney-Rangoli":"midjourney",
            # "models/hakurei/waifu-diffusion":"waifu-diffusion",
            # "models/Linaqruf/anything-v3.0":"anything-v3.0",
           }

tab_actions = []
tab_titles = []
for model_id in model_ids.keys():
    print(model_id, model_ids[model_id])
    try:
        tab = gr.Interface.load(model_id)
        tab_actions.append(tab)
        tab_titles.append(model_ids[model_id])
    except:
        logger.info(f"load_fail__{model_id}_")
        
def chat(api, input0, input1, chat_radio, chat_history):
    out_chat = []
    if chat_history != '':
        out_chat = json.loads(chat_history)
    logger.info(f"out_chat_: {len(out_chat)} / {chat_radio}")
    if chat_radio == "Talk to chatGPT":
        response = get_response_from_chatbot(api, input0)
        out_chat.append((input0, response))
        chat_history = json.dumps(out_chat)
        return api, out_chat, input1, chat_history
    else:
        prompt_en = getTextTrans(input0, source='zh', target='en') + f',{random.randint(0,sys.maxsize)}'
        return api, out_chat, prompt_en, chat_history

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
    function save_conversation(chatbot) {        
        var conversations = new Array();
        for (var i = 0; i < chatbot.children.length; i++) {
            conversations[i] = chatbot.children[i].innerHTML;
        }
        var json_str = JSON.stringify(conversations);
        localStorage.setItem('chatgpt_conversations', json_str);
    }
    function load_conversation(chatbot) {
        var json_str = localStorage.getItem('chatgpt_conversations');
        if (json_str) {
            conversations = JSON.parse(json_str);
            for (var i = 0; i < conversations.length; i++) {
                var new_div = document.createElement("div");
                if((i%2)===0){
                    new_div.className = "px-3 py-2 rounded-[22px] rounded-br-none text-white text-sm chat-message svelte-rct66g";
                    new_div.style.backgroundColor = "#16a34a"; 
                } else {
                    new_div.className = "px-3 py-2 rounded-[22px] rounded-bl-none place-self-start text-white text-sm chat-message svelte-rct66g";
                    new_div.style.backgroundColor = "#2563eb"; 
                    if (conversations[i].indexOf("<img ") == 0) { 
                        new_div.style.width = "80%"; 
                        new_div.style.padding = "0.2rem"; 
                    }                
                }
                new_div.innerHTML = conversations[i];
                chatbot.appendChild(new_div);
            }
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
            output_htmls = window['gradioEl'].querySelectorAll('.output-html');
            for (var i = 0; i < output_htmls.length; i++) {
               output_htmls[i].style.display = "none";
            }
            new_height = (clientHeight - 250) + 'px';
        } else {
            new_height = (clientHeight - 350) + 'px';
        }
        chat_row.style.height = new_height;
        window['chat_bot'].style.height = new_height;
        window['chat_bot'].children[2].style.height = new_height;
        window['chat_bot1'].style.height = new_height;
        window['chat_bot1'].children[2].style.height = new_height;
        prompt_row.children[0].style.flex = 'auto';
        prompt_row.children[0].style.width = '100%';
        window['gradioEl'].querySelectorAll('#chat_radio')[0].style.flex = 'auto';
        window['gradioEl'].querySelectorAll('#chat_radio')[0].style.width = '100%';        
        prompt_row.children[0].setAttribute('style','flex-direction: inherit; flex: 1 1 auto; width: 100%;border-color: green;border-width: 1px !important;')
        window['chat_bot1'].children[1].setAttribute('style', 'border-bottom-right-radius:0;top:unset;bottom:0;padding-left:0.1rem');
        load_conversation(window['chat_bot1'].children[2].children[0]);
        window['chat_bot1'].children[2].scrollTop = window['chat_bot1'].children[2].scrollHeight;
        var mousedown_last = 0;
        window['chat_bot1'].children[2].addEventListener('mousedown', function(e) {
            mousedown_last = new Date();
        })
        window['chat_bot1'].children[2].addEventListener('mouseup', function(e) {
            var now = new Date();
            if (now - mousedown_last > 5 * 1000) {
                if (confirm('Clear outputs?')==true) {
                     window['chat_bot1'].children[2].children[0].innerHTML = '';
                     save_conversation(window['chat_bot1'].children[2].children[0]);
                }
            }
            mousedown_last = 0;
        })
 
        window['prevPrompt'] = '';
        window['doCheckPrompt'] = 0;
        window['prevImgSrc'] = '';
        window['checkChange'] = function checkChange() {
            try {
                if (window['gradioEl'].querySelectorAll('.gr-radio')[0].checked) {
                    if (window['chat_bot'].children[2].children[0].children.length > window['div_count']) {
                        new_len = window['chat_bot'].children[2].children[0].children.length - window['div_count'];
                        for (var i = 0; i < new_len; i++) { 
                            new_div = window['chat_bot'].children[2].children[0].children[window['div_count'] + i].cloneNode(true);
                            window['chat_bot1'].children[2].children[0].appendChild(new_div);
                        }
                        window['div_count'] = chat_bot.children[2].children[0].children.length;
                        window['chat_bot1'].children[2].scrollTop = window['chat_bot1'].children[2].scrollHeight;
                        save_conversation(window['chat_bot1'].children[2].children[0]);
                    }
                    if (window['chat_bot'].children[0].children.length > 1) {
                        window['chat_bot1'].children[1].textContent = window['chat_bot'].children[0].children[1].textContent;
                    } else {
                        window['chat_bot1'].children[1].textContent = '';
                    }
                } else {
                    texts = window['gradioEl'].querySelectorAll('textarea');
                    text0 = texts[0];    
                    text1 = texts[1];
                    img_index = 0;
                    if (window['doCheckPrompt'] === 0 && window['prevPrompt'] !== text1.value) {
                            console.log('_____new prompt___[' + text1.value + ']_');
                            window['doCheckPrompt'] = 1;
                            window['prevPrompt'] = text1.value;
                            for (var i = 3; i < texts.length; i++) {
                                setNativeValue(texts[i], text1.value);
                                texts[i].dispatchEvent(new Event('input', { bubbles: true }));
                            }                        
                            setTimeout(function() {
                                img_submit_btns = window['gradioEl'].querySelectorAll('#tab_img')[0].querySelectorAll("button");
                                for (var i = 0; i < img_submit_btns.length; i++) {
                                    if (img_submit_btns[i].innerText == 'Submit') {
                                        img_submit_btns[i].click();                
                                    }
                                }
                                window['doCheckPrompt'] = 0;
                            }, 10);                   
                    }
                    tabitems = window['gradioEl'].querySelectorAll('.tabitem');
                    imgs = tabitems[img_index].children[0].children[1].children[1].children[0].querySelectorAll("img");
                    if (imgs.length > 0) {
                        if (window['prevImgSrc'] !== imgs[0].src) {
                            var user_div = document.createElement("div");
                            user_div.className = "px-3 py-2 rounded-[22px] rounded-br-none text-white text-sm chat-message svelte-rct66g";
                            user_div.style.backgroundColor = "#16a34a"; 
                            user_div.innerHTML = "<p>" + text0.value + "</p>";
                            window['chat_bot1'].children[2].children[0].appendChild(user_div);
                            var bot_div = document.createElement("div");
                            bot_div.className = "px-3 py-2 rounded-[22px] rounded-bl-none place-self-start text-white text-sm chat-message svelte-rct66g";
                            bot_div.style.backgroundColor = "#2563eb"; 
                            bot_div.style.width = "80%"; 
                            bot_div.style.padding = "0.2rem"; 
                            bot_div.appendChild(imgs[0].cloneNode(true));
                            window['chat_bot1'].children[2].children[0].appendChild(bot_div);
                            
                            window['chat_bot1'].children[2].scrollTop = window['chat_bot1'].children[2].scrollHeight;
                            window['prevImgSrc'] = imgs[0].src;
                            save_conversation(window['chat_bot1'].children[2].children[0]);
                        }
                    }
                    if (tabitems[img_index].children[0].children[1].children[1].children[0].children[0].children.length > 1) {
                         window['chat_bot1'].children[1].textContent = tabitems[img_index].children[0].children[1].children[1].children[0].children[0].children[1].textContent;
                    } else {
                        window['chat_bot1'].children[1].textContent = '';
                    }                              
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
            prompt_input0 = gr.Textbox(lines=2, label="prompt",show_label=False)
            prompt_input1 = gr.Textbox(lines=4, label="prompt", visible=False)
            chat_history = gr.Textbox(lines=4, label="prompt", visible=False)
            chat_radio = gr.Radio(["Talk to chatGPT", "Text to Image"], elem_id="chat_radio",value="Talk to chatGPT", show_label=False)
            submit_btn = gr.Button(value = "submit",elem_id="submit-btn").style(
                    margin=True,
                    rounded=(True, True, True, True),
                    width=100
                )
            api = gr.State(value=get_api())
            submit_btn.click(fn=chat, 
                             inputs=[api, prompt_input0, prompt_input1, chat_radio, chat_history], 
                             outputs=[api, chatbot, prompt_input1, chat_history],
                            )
        with gr.Row(elem_id='tab_img', visible=False).style(height=5):
           tab_img = gr.TabbedInterface(tab_actions, tab_titles)             

demo.launch(debug = True)
