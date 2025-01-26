from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

class HeyBotCommand:
    async def handle_hey_bot_command(ctx):
        print(ctx.message.author)
        template = """You are a helpfulp chat assistant that is knowledgable about mainly programming. This is my Discord chat channel, where I host documentation for the Cryptographic API Services Github Organization.
        It is a cryptography project that encompasses C#, TypeScript, and Rust. In some instances, a chat history will be 
        provided to you from the user who is chatting with you, you are to answer questions to the best of your ability. There is no such thing as a newbie question, you are to answer them all.
        Question: {question}"""
        prompt = ChatPromptTemplate.from_template(template)
        model = OllamaLLM(model="llama3.2")
        chain = prompt | model
        stripped_message = ctx.message.content.replace("!heybot", "")
        llm_response = chain.invoke({"question": stripped_message})
        await ctx.send(llm_response)