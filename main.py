import os; os.environ['no_proxy'] = '*' # 避免代理网络产生意外污染
import gradio as gr
from rx import predict


# 如果WEB_PORT是-1, 则随机选取WEB端口
PORT = 5000

title_html = """<h1 align="center">Chatbot</h1>"""

# 问询记录, python 版本建议3.9+（越新越好）
import logging
os.makedirs('gpt_log', exist_ok=True)
try:logging.basicConfig(filename='gpt_log/chat_secrets.log', level=logging.INFO, encoding='utf-8')
except:logging.basicConfig(filename='gpt_log/chat_secrets.log', level=logging.INFO)
print('所有问询记录将自动保存在本地目录./gpt_log/chat_secrets.log, 请注意自我隐私保护哦！')


# 保存API_KEY
API_KEY = "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"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def saveHeader(API_KEY):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    print(headers)
    return headers

with gr.Blocks(analytics_enabled=False) as demo:
    gr.HTML(title_html)
    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot()
            chatbot.style(height=1000)
            chatbot.style()
            history = gr.State([])
            TRUE = gr.State(True)
            FALSE = gr.State(False)
        with gr.Column(scale=1):
            with gr.Row():
                with gr.Column():
                    txt = gr.Textbox(show_label=False, placeholder="Input question here.").style(container=False)
                with gr.Column():
                    submitBtn = gr.Button("提交", variant="primary")
                with gr.Row():
                    resetBtn = gr.Button("重置", variant="secondary");
                    resetBtn.style(size="sm")
                    stopBtn = gr.Button("停止", variant="secondary");
                    stopBtn.style(size="sm")
    cancel_handles = []
    input_combo = [txt, chatbot, history]
    output_combo = [chatbot, history]
    predict_args = dict(fn=predict, inputs=input_combo, outputs=output_combo)
    empty_txt_args = dict(fn=lambda: "", inputs=[], outputs=[txt])  # 用于在提交后清空输入栏

    # 提交按钮、重置按钮
    cancel_handles.append(txt.submit(**predict_args))  # ; txt.submit(**empty_txt_args) 在提交后清空输入栏
    cancel_handles.append(submitBtn.click(**predict_args))  # ; submitBtn.click(**empty_txt_args) 在提交后清空输入栏
    resetBtn.click(lambda: ([], [], "已重置"), None, output_combo)



# 延迟函数, 做一些准备工作, 最后尝试打开浏览器
def auto_opentab_delay():
    import threading, webbrowser, time
    print(f"URL http://localhost:{PORT}")
    def open(): time.sleep(2)
    webbrowser.open_new_tab(f'http://localhost:{PORT}')
    t = threading.Thread(target=open)
    t.daemon = True; t.start()

auto_opentab_delay()
demo.title = "Chatbot"
demo.queue().launch(server_name="0.0.0.0", share=False, server_port=PORT)
