from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq


load_dotenv()

llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")


if __name__ == "__main__":
    response = llm.invoke("What are the two main ingredients in samosa")
    print(response.content)