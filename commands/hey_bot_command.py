from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

class HeyBotCommand:
    async def handle_hey_bot_command(ctx):
        template = """Question: {question}"""
        prompt = ChatPromptTemplate.from_template(template)
        model = OllamaLLM(model="llama3.2")
        chain = prompt | model
        stripped_message = ctx.message.content.replace("!heybot", "")
        llm_response = chain.invoke({"question": stripped_message})
        await ctx.send(llm_response)