import zipfile
import gradio as gr
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    ChatPromptTemplate
)
from langchain_core.output_parsers import StrOutputParser
import os

# Load env
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("groq_key")

# Model
model = init_chat_model(
    "groq:llama-3.1-8b-instant",
    temperature=0.3,
    max_tokens=5000
)

# System Prompt
sys_temp = """
You are a Senior frontend developer with 20 years experience.
Generate production-ready frontend code.
MANDATORY FORMAT: (Exact delimeters)
--html--
[HTML code here]
--html--
--css--
[CSS code here]
--css--
--js--
[java script code here]
--js--
name should be index.html, styles.css, script.js only.
"""

hum_temp = "Build a {description} using following {content}"

sys_msg = SystemMessagePromptTemplate.from_template(sys_temp)
hum_msg = HumanMessagePromptTemplate.from_template(hum_temp)

chat_template = ChatPromptTemplate.from_messages([sys_msg, hum_msg])
parser = StrOutputParser()

chain = chat_template | model | parser


# Safe Extract Function



# Main Function
def generate_frontend(description, content):
    response = chain.invoke({
        "description": description,
        "content": content
    })

    html = response.split('--html--')
    css = response.split('--css--')
    js = response.split('--js--')

    # Create zip
    zip_filename = "frontend_project.zip"
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        zipf.writestr("index.html", html[1])
        zipf.writestr("styles.css", css[1])
        zipf.writestr("script.js", js[1])

    return zip_filename


# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# AI Frontend Code Generator")

    description_input = gr.Textbox(label="Project Description", lines=6)
    content_input = gr.Textbox(label="Project Content", lines=10)

    generate_btn = gr.Button("Generate & Download")

    output_file = gr.File(label="Download ZIP")

    generate_btn.click(
        fn=generate_frontend,
        inputs=[description_input, content_input],
        outputs=output_file
    )

demo.launch()
