from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import select
from langchain_community.vectorstores import PGVector
from pgvector.sqlalchemy import Vector
from langchain.schema import Document
from sqlalchemy.sql import func
from database.database import get_pgvector_connection  # Assuming you have this function

class HeyBotCommand:
    async def handle_hey_bot_command(ctx):
        # Clean the message to remove the bot command
        stripped_message = ctx.message.content.replace("!heybot", "")

        # Generate the query embedding using Ollama embeddings
        ollama_embeddings = OllamaEmbeddings(model='llama3.2')
        query_embedding = ollama_embeddings.embed_query(stripped_message)
        query_embedding_vector = func.cast(query_embedding, Vector(3072))
        # Establish database connection using SQLAlchemy
        session = get_pgvector_connection()
        session_instance = session()

        # Reflect the documents table using SQLAlchemy
        metadata = MetaData()
        documents_table = Table('Documents', metadata, autoload_with=session_instance.get_bind())

        # Create the SQL query to fetch the most relevant document(s) using PGVector similarity search
        statement = select(documents_table.c.id, documents_table.c.text, documents_table.c.embedding) \
                    .order_by(documents_table.c.embedding.op("<=>")(query_embedding_vector)) \
                    .limit(5)  # You can change this to fetch more results

        result = session_instance.execute(statement).fetchall()
        session_instance.close()

        # Prepare the documents retrieved for the VectorStore
        documents = [Document(page_content=row[1]) for row in result]

        # Create a vector store from the documents using Ollama embeddings
        vectorstore = PGVector.from_documents(documents, ollama_embeddings, connection_string=session_instance.bind.url)

        # Create a retriever using the vector store
        retriever = vectorstore.as_retriever()  # Use the `as_retriever()` method to turn the vector store into a retriever

        # Set up Ollama LLM model (replace with the actual model and API key)
        llm = OllamaLLM(model="llama3.2")

        # Set up the QA Chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",  # Stuff the documents into the prompt
            retriever=retriever
        )

        # Generate the answer based on the query
        answer = qa_chain.invoke(stripped_message)
        # Send the generated answer as a response
        await ctx.send(answer['result'])
