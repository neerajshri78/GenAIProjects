from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

load_dotenv()

template= """ Telle me a Joke on {question} """ 
prompt=ChatPromptTemplate.from_template(template)

llm=ChatOllama(temprature=30,model="llama3.1") 

#llm = ChatOpenAI(temperature=0, model="gpt-4o")

chain=prompt|llm

response=chain.invoke({"question":"space"})
print(response.content)


