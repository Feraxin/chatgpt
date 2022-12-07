from pyChatGPT import ChatGPT
import os


def read_token():
  session_token_text="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..rZTgbQYSLSN-fX8o.N74lAfJIiSxsXjb6I8EEIQscpXJpSXdTOfUmUTTeqnhRxmuVCuAz_lFcrk8_9H7Pk4dWGKQaxW4EViyWXfp8tgiuQJZJCMd9N-2mKouGIKQWxXYaaHnJwusalk1Opl2pjCWerIvWlRDC5kG5-C0iRrxNd3hgFoRURRBcQXm_Fk7B2TO6jIoVdGdpA61MbwesIAxn1NkgZYpxVTUc847a0LByWdx5r0PVgymxbOfidLtIdA3T6nPXnxjI1qkxiQH7Xts7II_GiNcRnQ69-686E_JW3PFmez-LhEZiSOYMriMbqdZh_szrtFIofZPW4mX6BzyTQODay4li5-0RCiarzbZId2fjbylFuq3z6TfTnCyhloYIG_h0fJ0JECWE6jKnEkIg--pdQwtnDqEYdfxm2m0iYSrxqpPioCiB2qN6s4sYLQ-u0G7dPc9zFN50V8tMfPHkoaIh7TGLoCJSuqe0cEs1x2wVVMDunmnVBMSdfKhF1NizInKZ9ojiL7fgrRggw-Rz0zXdHjMFfCI9n0ZaWM3AUZPJoB2ZUT24_bYjaMDce-2cdrhJQGYiMKSq2dK0xiyklKZ9_2naqShyAMkstDR7SHelsfesTn7zmQO2KxOMwyxwKSB8rTY3GCftIwItJRVCtxxE8z5-21joDa1sujixO8Fq2UGmZiq0CpY-5lpo_a3bUr-Ut1rNmN_1zukPdVfLiL-a9YoCWr7H8bDCerk54gFdArtUZ7kF47DzgxDcvSdtCho5H26h0OAkJ125cbHIrTiotoRpzsaUxtsqv-gsucYZfyTaTq76TwC8X0rpJPljK6hGfu9U_nC5u0QLVQfaINO1PR9IyzsFmgdYupM2ecvNdQY_1IzBGl1FVo5y2cr-eb-CzBZMxAU7lI7D1bsu8p3Vwyxg_pZ1S8uUtUwo9evWOc6vaDVct1J3HiAZ_rjl3iA3c7XsjyuoXAnRarS6pEVIN-HH91eF2DysNRgeCTaFnRdBx3Saq1EJVtl_WCiIXnuYG9ZChLmuiVXUFrs_WDmRDADhQJ1Kr8DT_5gIEekGRCz9c5cvMoQXF58O-Mr0vxghXzXjw1LtN0iwhyJoZYeI0RU8ITwZZcggOoU8vyc68ipqbUqIcilEVLu_NN7sT1UqnlAYoff3A0mjBOZWWERbK2W7rKm4MlWc_RwhZze7Au-uJRSdY6jngdPZpDvVxbqf7SjCok0qPzyH-n9QHwd0QrPSVNoPodIGdz6UX_9EnRsiwhVvwtjLPVGksicdTU-2mz4AdAvoMHqovebIkfWPYudcgM2v3qIkaP-1nfDnD5rjipK1xL3S3xCroZh7lRztOCQpMSrjCUi0KrzCZydFQYrsm0487WnEaqKnLBiX_QKM-I0brmF8NCG1YKkgPSuTQlW-WiYKKtFFGZ4T0DuQYGLDP89-iKih48gQ8-OB1IjOIYt9HU-6RiqUakgvS-Mq7WAKFxwifW2XHUZAUeCeyMQ_awa64ROC12AAdB8rFP8GScq0E_vRuXcHsdW_ENJaFK9zDNaNJhBQTv4GOkUO8Xb8lbEARZmHlZYqM04rcMV6x_4LzYEK75Kx_CAMdXdH430AC1-G638GW0ogvUODG4PsT6FJask0eeSVwBrS3Ndv_v8SgHbl2HnNvZDVaANblTGVWX-subHyf-K18ZlA7rH7XBm8QhtsJYHGgyGzettXl729z7AdVMo36MCMpoOywwCNER1iBderWGNf2NKOTo6uLNd4dnmveaO3GyF7z84Te-xgBP9iJUhkIR7hxiJOMR4b6ofjvMN1o24UkwCJ3A_vVu0hW0ZqCrnSJqnRKJTnXH3cWWZuZsHA8RvMTb8igieTbQswtFA3ZHP77ZqEHnT5JwgjJr-0kBc9fWeqH9N0b1f-mavTtjg0Xi7gO69T2olaIC9d1ruFBfI0ZWuu9cHjmirfjvOLzSbg03Gj5peZ_7N0g-JlHU36nQuZwizQEzOxR1-qH1YC2zFsmQ-VfnRSfKzTOcbZkaubks4c2XzqFckEygiqGDBi9wqMicfSTROdC4E_UXY0t4XQIdJC5HcGYQwgIYF0QdJJUBgvClSyuS9DIpbAckLj_BlfOLsfBnSsRd1oNvj1VTQSqq_7nT0Bv1u0cMeQy_3WGPAAdHvi8GP_qFxS6XqYr8luQc7_KhMIytY2fEFJISjZRpRr1zOu3qYGAiSXx9Emd7NAvjY1v0cQn11-vqdlZRM1Qz7lY8bexnOkfjjKVBQ5otsJ9s7sR5LU._A5iHP30u_uJKApc_1-TLg"

  # with open("session_token.txt") as fd:
  #   session_token = fd.read()

  return  session_token_text


def chat(text,session_tokenz):

    try:
      //loaded_session_token = os.environ['Newkeyz']
      
      session_token = read_token()
      
      api = ChatGPT(session_token) 
      resp = api.send_message(text)
    
      api.refresh_auth() 
      api.reset_conversation() 
      xyz = resp['message']
    except:
 
        api = ChatGPT(session_tokenz)
        resp = api.send_message(text)

        api.refresh_auth() 
        api.reset_conversation()  

    return xyz


 
import gradio as gr
gr.Interface(chat,
              inputs = [gr.Textbox(label = ' 输入问题： '),
               gr.Textbox(label = ' 如果失败，你可以填写自己的session-token')], 
               outputs = gr.outputs.Textbox(type="text",label="ChatGPT 回复你了："), 
               title = "ChatGPT 中文",
               description= "").launch(debug = True)