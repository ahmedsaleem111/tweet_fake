import gradio as gr

def social_summary(username, year):
    # model()
    return "output here..."

with gr.Blocks() as ui:
    with gr.Row():
        with gr.Column():
            username = gr.Textbox(label="Twitter username:")
            year = gr.Textbox(label="Specify year:")
            button = gr.Button(value="Wrap the Year")
        with gr.Column():
            summary = gr.Textbox(label="Summary")

    button.click(social_summary, inputs=[username, year], outputs=summary)
    examples = gr.Examples(examples=[["test1", "2022"], ["test2", "2021"]], inputs=[username, year])

ui.launch()
