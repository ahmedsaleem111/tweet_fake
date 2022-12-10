import gradio as gr

def social_summary(username_ig, password_ig, username_twitter, password_twitter, year):
    # model()
    return "output here..."

with gr.Blocks() as ui:
    with gr.Row():
        with gr.Column():
            username_ig = gr.Textbox(label="Instagram username:")
            password_ig = gr.Textbox(label="Instagram password:")
            username_twitter = gr.Textbox(label="Twitter username:")
            password_twitter = gr.Textbox(label="Twitter password:")
            year = gr.Textbox(label="Specify year:")
            button = gr.Button(value="Wrap the Year")
        with gr.Column():
            summary = gr.Textbox(label="Summary")

    button.click(social_summary, inputs=[username_ig, password_ig, username_twitter, password_twitter, year], outputs=summary)

ui.launch()
