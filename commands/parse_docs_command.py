from langchain_ollama.embeddings import OllamaEmbeddings
import git
import os
from database.database import get_pgvector_connection
from sqlalchemy.sql import insert
from sqlalchemy import Table, MetaData
import shutil

class ParseDocsCommand:
    async def parse_docs(ctx):
        # Getting session
        session = get_pgvector_connection()
        session_instance = session()

        # Get the table or model for documents (Make sure it's defined properly)
        metadata = MetaData()
        documents_table = Table('Documents', metadata, autoload_with=session_instance.get_bind())
        repo_path = "https://github.com/R4ptX/Resources"

        delete_statement = documents_table.delete()
        session_instance.execute(delete_statement)
        session_instance.commit()

        local_path = os.path.join(os.getcwd(), "repo.git")
        repo = git.Repo.clone_from(repo_path, local_path)

        # Get all the markdown files
        md_files = []
        for root, dirs, files in os.walk(repo.working_tree_dir):
            for file in files:
                if file.endswith('.md'):
                    md_files.append(os.path.join(root, file))

        #read all file paths into memory
        docs = []
        for md_file in md_files:
            with open(md_file, "r", encoding="utf-8") as file:
                content = file.read()
                docs.append(content)

        # Generate embeddings
        embeddings = OllamaEmbeddings(model='llama3.2')
        embedded_docs = embeddings.embed_documents(docs)

        # Insert data
        insert_data = []
        for i, doc in enumerate(docs):
            embedding = embedded_docs[i]  # Get the embedding corresponding to the document
            insert_data.append({'text': doc, 'embedding': embedding})

        # Insert statement
        statement = insert(documents_table).values(insert_data)
        session_instance.execute(statement)

        # Commit the transaction using the session
        session_instance.commit()

        # Close the session
        session_instance.close()
        shutil.rmtree(local_path)
        # Send confirmation message
        await ctx.send("Docs successfully reloaded")
