from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader
from langchain_ollama.llms import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain.schema import Document
import git
import os
import shutil

class ParseDocsCommand:
    async def parse_docs(ctx):
        repo_path = "https://github.com/R4ptX/Resources"
        local_path = os.path.join(os.getcwd(), "repo.git")
        repo = git.Repo.clone_from(repo_path, local_path)
        # Get a list of all MD files in the repository
        md_files = []
        for root, dirs, files in os.walk(repo.working_tree_dir):
            for file in files:
                if file.endswith('.md'):
                    md_files.append(os.path.join(root, file))
        docs = []
        for md_file in md_files:
            with open(md_file, "r", encoding="utf-8") as file:
                content = file.read()
                docs.append(Document(page_content=content))
        embeddings = OllamaEmbeddings(model='llama3.2')
        model = OllamaLLM(model="llama3.2")
        store = FAISS.from_documents(docs, embeddings)

        # Set up a simple question-answering chain using LangChain
        qa_chain = RetrievalQA.from_chain_type(
            llm=model,  
            chain_type="stuff",
            retriever=store.as_retriever()
        )
        result = qa_chain.invoke('In the provided context, what are some good pod casts?')
        shutil.rmtree(local_path)
        await ctx.send(result['result'])
