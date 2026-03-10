# PocketAI

PocketAI is a **local AI assistant** that combines conversational AI, coding assistance, document question answering, and tool execution in a single system. It runs open-source language models locally using **Ollama**, allowing users to interact with an AI assistant without relying on external APIs.

The project demonstrates how a modern AI assistant can be built locally by integrating:

```
Language Model + Conversation Memory + Retrieval (RAG) + Tools + Interface
```

PocketAI is designed to be:

- Local-first
- Lightweight
- Modular
- Extensible
- Open-source friendly

---

# Features

## Conversational AI

PocketAI supports natural language interaction with a local language model.

Capabilities include:

- General question answering
- Context-aware responses
- Multi-turn conversations
- Programming help
- Code explanation

---

## Conversation Memory

PocketAI maintains conversation context so the assistant can remember earlier parts of a conversation and respond appropriately to follow-up questions.

Example:

```
User: My favorite programming language is C++.
User: What is my favorite programming language?
AI: C++
```

This allows the assistant to maintain **context across messages during a session**, making conversations more natural.

---

## Coding Assistance

PocketAI can assist with programming tasks including:

- Code generation
- Code debugging
- Code explanation
- Algorithm discussion

Supported languages include:

```
Python
C
C++
Java
```

Example:

```
User: write a binary search in C++
AI: returns the implementation with explanation
```

---

## Document Question Answering

PocketAI supports **document-based question answering** using Retrieval Augmented Generation (RAG).

Users can upload documents and ask questions about their contents.

Supported file formats:

```
PDF
TXT
Markdown
```

Document processing workflow:

```
Load document
Split text into chunks
Generate embeddings
Store vectors in a vector database
Retrieve relevant sections during queries
```

Example:

```
User: summarize section 2 of the uploaded document
AI: generated summary based on retrieved document context
```

---

## Tool Integration

PocketAI can automatically use tools when required.

Available tools:

```
Calculator
Python Code Execution
Web Search
```

### Calculator

Performs mathematical calculations.

Example:

```
calculate 45 * 21
```

Output:

```
945
```

---

### Python Execution

Executes Python code directly from the chat.

Example:

```
run python print(2+2)
```

Output:

```
4
```

---

### Web Search

Retrieves current information using DuckDuckGo.

Example:

```
search latest AI regulation news
```

Search results are summarized by the language model.

---

# Technology Stack

## Runtime

```
Ollama
```

## Models

```
mistral
phi3
codellama
```

## Framework

```
LangChain
```

## Vector Database

```
Chroma
```

## Embeddings

```
nomic-embed-text
all-minilm
```

## Web Search

```
DuckDuckGo (ddgs)
```

## Interface

```
Gradio
```

---

# Project Structure

```
PocketAI/

app.py

config.py

index_documents.py

ui/
    chat_ui.py

llm/
    llm_loader.py

memory/
    memory_manager.py

rag/
    document_loader.py
    text_splitter.py
    embeddings.py
    vector_store.py
    retriever.py

agents/
    tool_agent.py

tools/
    calculator.py
    python_executor.py
    web_search.py

data/
    documents/
    vector_db/

```

---

# Installation

Clone the repository, then:

```
cd pocketai
```

Create a virtual environment:

```
python -m venv venv
```

Activate the environment.

Windows:

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Install Ollama

Download Ollama from:

```
https://ollama.com
```

Pull required models:

```
ollama pull mistral
ollama pull phi3
ollama pull nomic-embed-text
```

Verify installation:

```
ollama list
```

---

# Running PocketAI

Run the assistant from terminal:

```
python app.py
```

Example interaction:

```
You: calculate 20 percent of 50
AI: 10
```

Exit with:

```
exit
```

---

# Running the Web Interface

Launch the web interface:

```
python ui/chat_ui.py
```

The interface runs locally at:

```
http://127.0.0.1:7860
```

---

# Hardware Requirements

Minimum:

```
8 GB RAM
```

Recommended:

```
16 GB RAM
```

Example model sizes:

```
phi3      ~2.2 GB
mistral   ~4.4 GB
```

GPU acceleration is optional but can improve performance.

---

# Summary

PocketAI demonstrates how a complete AI assistant can be built locally by combining:

```
Local Language Models
Conversation Memory
Document Retrieval
External Tools
Interactive Interface
```

The system is modular and can be extended with additional models, tools, or capabilities.
