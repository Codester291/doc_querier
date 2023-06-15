from langchain.agents import (load_tools, initialize_agent)
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.vectorstores import Pinecone
from langchain.document_loaders import UnstructuredURLLoader
from models import ResponseModel
import pinecone
import os
from dotenv import load_dotenv

#load env variables
load_dotenv()

#initialize pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), 
    environment=os.getenv("PINECONE_ENV")
)

def perform_queries(url: str, query: str):

    #load texts
    url_loader = UnstructuredURLLoader(urls=[url])
    loader = TextLoader("./output.txt")
    documents = url_loader.load()

    #Split texts
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents=documents)

    #initialize Embeddings
    embeddings = OpenAIEmbeddings()

    index_name = "analyzefile"

    #Search Docs
    docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    result = docsearch.similarity_search(query)
    print(f"Result:{result}")
    
    return ResponseModel(code="00", message="Successful", data={"content": result[0].page_content})

# llm = OpenAI(temperature=0.9)
# h_llm = HuggingFaceHub(repo_id="google/flan-t5-large", model_kwargs={"temperature": 0, "max_length": 64})
# tools = load_tools(["wikipedia", "llm-math"], llm=llm)
# conversation = ConversationChain(llm=llm, verbose=True)

# agent = initialize_agent(tools=tools, llm=llm, agent="zero-shot-react-description", verbose=True)

# template = """Question: {question}
# Let's think step by step
# Answer: """

# prompt = PromptTemplate(template=template, input_variables=["question"])
# question="What are the major types of PC you would recommend for a programmer?"

# llm_chain = LLMChain(prompt=prompt, llm=llm)
# # print(f"{agent.run('What year was the anime Evangelion released? multiply 2 and 2')}")
# print(f"{converstaion.predict(input='Can we talk about AI?')}")

