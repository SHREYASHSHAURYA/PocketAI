from llm.llm_loader import generate_response
from memory.memory_manager import MemoryManager
from rag.retriever import retrieve_context
from agents.tool_agent import try_tool

memory = MemoryManager()

SYSTEM_PROMPT = """
You are PocketAI, a helpful AI assistant.

Capabilities:
- Answer general questions
- Help with programming
- Explain code
- Debug code
- Write code in Python, C, C++, Java and other languages

Rules:
- Only generate code when the user asks for programming help.
- When writing code, always format it inside proper code blocks.
- Keep explanations clear and concise.
"""

while True:
    print("You: ", end="")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    user_input = "\n".join(lines).strip()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        break


    tool_result = try_tool(user_input)

    if tool_result is not None:
  
        if tool_result.startswith("Web search results:"):

            user_message = f"""
    Answer the question using the web search results below.
    Give a short and direct answer.

    {tool_result}

    Question: {user_input}
    """

            messages = (
                [{"role": "system", "content": SYSTEM_PROMPT}]
                + memory.get_messages()
                + [{"role": "user", "content": user_message}]
            )

            response = generate_response(messages)

            print("AI:", response)

            memory.add_user_message(user_input)
            memory.add_ai_message(response)

        else:
            print("AI:", tool_result)
            memory.add_user_message(user_input)
            memory.add_ai_message(tool_result)

        continue


    context = retrieve_context(user_input)

    if context:
        user_message = f"""
        Use the following document context to answer the question.

        If the answer is not in the context, say you do not know.

        Context:
        {context}

        Question: {user_input}
        """
    else:
        user_message = user_input

    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + memory.get_messages()
        + [{"role": "user", "content": user_message}]
    )

    response = generate_response(messages)

    lower_response = response.lower()

    uncertain_phrases = [
        "i don't know",
        "i do not know",
        "not sure",
        "cannot find",
        "no information",
        "as of my last update",
        "i don't have real-time",
        "i do not have real-time",
        "i don't have access"
    ]

    if any(p in lower_response for p in uncertain_phrases):

        from tools.web_search import web_search

        results = web_search(user_input)

        if results:

            user_message = f"""
    Answer the question using the web search results below.
    Give a short and direct answer.

    {results}

    Question: {user_input}
    """

            messages = (
                [{"role": "system", "content": SYSTEM_PROMPT}]
                + memory.get_messages()
                + [{"role": "user", "content": user_message}]
            )

            response = generate_response(messages)

    print("AI:", response)

    memory.add_user_message(user_input)
    memory.add_ai_message(response)













