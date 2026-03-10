import sys
import os
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import gradio as gr

from llm.llm_loader import generate_response
from memory.memory_manager import MemoryManager
from rag.retriever import retrieve_context
from agents.tool_agent import try_tool
from tools.web_search import web_search
from rag.document_loader import load_documents
from rag.text_splitter import split_documents
from rag.embeddings import get_embeddings
from rag.vector_store import create_vector_store

SYSTEM_PROMPT = """
You are PocketAI, a helpful AI assistant.

Capabilities:
- Answer general questions
- Help with programming
- Explain code
- Debug code
- Write code in Python, C, C++, Java and other languages

Rules:
- Only generate code if the user explicitly asks for programming help or asks for code.
- If the user message is normal conversation, personal information, or a simple question, DO NOT generate code or programming examples.
- Never add programming examples unless the user clearly asks for code.
- When writing code, always format it inside proper code blocks.
- Keep explanations clear and concise.
"""

uncertain_phrases = [
    "i don't know",
    "i do not know",
    "not sure",
    "cannot find",
    "no information",
    "as of my last update",
    "i don't have real-time",
    "i do not have real-time",
    "i don't have access",
]

DOCS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "documents")
)
VECTOR_DB_DIR = "data/vector_db"


def index_uploaded_file(filepath):
    os.makedirs(DOCS_DIR, exist_ok=True)
    dest = os.path.join(DOCS_DIR, os.path.basename(filepath))
    shutil.copy2(filepath, dest)
    documents = load_documents(DOCS_DIR)
    chunks = split_documents(documents)
    embeddings = get_embeddings()
    create_vector_store(chunks, embeddings, VECTOR_DB_DIR)


def process_message(user_input, history, memory_state, upload_file, mode):

    user_input = (user_input or "").strip()

    if history is None:
        history = []

    if upload_file is not None:
        try:
            filepath = upload_file if isinstance(upload_file, str) else upload_file.name
            index_uploaded_file(filepath)

            history.append(
                {"role": "user", "content": f"📎 {os.path.basename(filepath)}"}
            )

        except Exception as e:
            history.append(
                {"role": "assistant", "content": f"Failed to index document: {str(e)}"}
            )

        upload_file = None

    if user_input:
        history = history + [{"role": "user", "content": user_input}]

    if not user_input:
        return "", history, memory_state, gr.update(value=None), mode

    if mode == "calculate":
        effective_input = f"calculate {user_input}"
    elif mode == "search":
        effective_input = f"search {user_input}"
    elif mode == "code":
        effective_input = f"write the code for: {user_input}"
    else:
        effective_input = user_input

    tool_result = try_tool(effective_input)

    if tool_result is not None:

        if tool_result.startswith("Web search results:"):

            user_message = f"""Answer the question using the web search results below.
Give a short and direct answer.

{tool_result}

Question: {effective_input}
"""

            messages = (
                [{"role": "system", "content": SYSTEM_PROMPT}]
                + memory_state.get_messages()
                + [{"role": "user", "content": user_message}]
            )

            response = generate_response(messages)

            memory_state.add_user_message(user_input)
            memory_state.add_ai_message(response)

        else:
            response = tool_result
            memory_state.add_user_message(user_input)
            memory_state.add_ai_message(tool_result)

        history.append({"role": "assistant", "content": response})
        return "", history, memory_state, gr.update(value=None), mode

    context = retrieve_context(effective_input or user_input)

    if context:
        user_message = f"""Answer the question ONLY using the document context below.

        If the answer is not present in the context, reply exactly:
        "Not found in document."

        Context:
        {context}

        Question:
        {effective_input  or user_input}
        """
    else:
        user_message = effective_input

    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + memory_state.get_messages()
        + [{"role": "user", "content": user_message}]
    )

    response = generate_response(messages)

    lower_response = response.lower()

    if any(p in lower_response for p in uncertain_phrases):

        results = web_search(effective_input)

        if results:

            user_message = f"""Answer the question using the web search results below.
Give a short and direct answer.

{results}

Question: {effective_input}
"""

            messages = (
                [{"role": "system", "content": SYSTEM_PROMPT}]
                + memory_state.get_messages()
                + [{"role": "user", "content": user_message}]
            )

            response = generate_response(messages)

    memory_state.add_user_message(user_input)
    memory_state.add_ai_message(response)

    history.append({"role": "assistant", "content": response})
    return "", history, memory_state, gr.update(value=None), mode


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

body {
    background: #06000d !important;
    font-family: 'Inter', sans-serif !important;
    margin: 0 !important;
    padding: 0 !important;
}

.gradio-container {
    background: #06000d !important;
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 24px 48px 32px 48px !important;
    font-family: 'Inter', sans-serif !important;
    min-height: 100vh !important;
}

#pocket-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 600;
    color: #c4b8dc;
    letter-spacing: 0.22em;
    font-family: 'Inter', sans-serif;
    margin: 0 0 4px 0;
    padding: 0;
}

#pocket-sub {
    text-align: center;
    font-size: 0.65rem;
    color: #40306a;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    margin: 0 0 20px 0;
    padding: 0;
    font-family: 'Inter', sans-serif;
}

#chatbot {
    background: #06000d !important;
    border: 1px solid #1a0a30 !important;
    border-radius: 12px !important;
}

.message-bubble-border {
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    line-height: 1.65 !important;
    padding: 12px 16px !important;
}

.user .message-bubble-border {
    background: #130828 !important;
    border: 1px solid #3a1a60 !important;
    color: #ddd4f4 !important;
}

.bot .message-bubble-border {
    background: #0d0b20 !important;
    border: 1px solid #1a1640 !important;
    color: #ddd4f4 !important;
}

.user .message-bubble-border *,
.bot .message-bubble-border * {
    color: #ddd4f4 !important;
}

.message-bubble-border pre {
    background: #050010 !important;
    border: 1px solid #2a1550 !important;
    border-radius: 8px !important;
    padding: 12px !important;
}

.message-bubble-border code {
    background: #050010 !important;
    border: 1px solid #2a1550 !important;
    border-radius: 4px !important;
    color: #b090f0 !important;
    font-size: 0.82rem !important;
}

.message-bubble-border pre code {
    border: none !important;
    background: transparent !important;
    color: #b090f0 !important;
}

#input-bar {
    background: #0a1530 !important;
    border-radius: 14px !important;
    border: 1px solid #162040 !important;
    padding: 14px 16px !important;
    margin-top: 14px !important;
}

#send-btn {
    background: linear-gradient(135deg, #1a0044, #4e00a0) !important;
    border: 1px solid #5800b8 !important;
    border-radius: 10px !important;
    color: #e0ccff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

#send-btn:hover {
    background: linear-gradient(135deg, #280060, #6800d0) !important;
    box-shadow: 0 0 16px rgba(100,0,200,0.4) !important;
}

footer { display: none !important; }
.built-with { display: none !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #06000d; }
::-webkit-scrollbar-thumb { background: #1c0e34; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #30185a; }
"""


def build_ui():
    with gr.Blocks(fill_height=True, title="PocketAI") as demo:

        memory_state = gr.State(MemoryManager())
        mode_state = gr.State("auto")

        gr.HTML(
            '<p id="pocket-title">PocketAI</p>'
            '<p id="pocket-sub">local &nbsp;·&nbsp; private &nbsp;·&nbsp; intelligent</p>'
        )

        chatbot = gr.Chatbot(
            elem_id="chatbot",
            show_label=False,
            height=520,
            render_markdown=True,
            autoscroll=True,
            placeholder=(
                "<div style='color:#2a1a4a;text-align:center;padding:80px 20px;"
                "font-family:Inter,sans-serif;font-size:0.9rem;'>Start a conversation</div>"
            ),
        )

        with gr.Column(elem_id="input-bar"):
            mode_display = gr.HTML(
                value="<div style='font-size:0.75rem;color:#6a50a0;padding:2px 0 6px 2px;'>mode: <b style='color:#b090f0'>auto</b></div>"
            )

            with gr.Row():
                auto_btn = gr.Button("auto", min_width=70, size="sm")
                code_btn = gr.Button("💻 code", min_width=80, size="sm")
                calculate_btn = gr.Button("🔢 calculate", min_width=100, size="sm")
                search_btn = gr.Button("🔍 search", min_width=80, size="sm")
                upload_btn = gr.Button("📎", min_width=36, size="sm")

            upload_file = gr.File(
                label="Upload document",
                file_types=[".pdf", ".txt", ".md", ".docx"],
                visible=False,
            )

            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Message PocketAI…",
                    lines=2,
                    max_lines=6,
                    show_label=False,
                    scale=8,
                )
                send_btn = gr.Button(
                    "Send ➤",
                    elem_id="send-btn",
                    scale=1,
                    min_width=90,
                )

        def set_mode(m):
            return (
                m,
                f"<div style='font-size:0.75rem;color:#6a50a0;padding:2px 0 6px 2px;'>mode: <b style='color:#b090f0'>{m}</b></div>",
            )

        auto_btn.click(fn=lambda: set_mode("auto"), outputs=[mode_state, mode_display])
        code_btn.click(fn=lambda: set_mode("code"), outputs=[mode_state, mode_display])
        calculate_btn.click(
            fn=lambda: set_mode("calculate"), outputs=[mode_state, mode_display]
        )
        search_btn.click(
            fn=lambda: set_mode("search"), outputs=[mode_state, mode_display]
        )
        upload_btn.click(fn=lambda: gr.update(visible=True), outputs=[upload_file])

        send_btn.click(
            fn=process_message,
            inputs=[msg_input, chatbot, memory_state, upload_file, mode_state],
            outputs=[msg_input, chatbot, memory_state, upload_file, mode_state],
        )

        msg_input.submit(
            fn=process_message,
            inputs=[msg_input, chatbot, memory_state, upload_file, mode_state],
            outputs=[msg_input, chatbot, memory_state, upload_file, mode_state],
        )

    return demo


if __name__ == "__main__":
    app = build_ui()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        css=CSS,
        max_threads=4,
    )
