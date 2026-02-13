import os
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


async def verify():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not found in .env or environment")
        return

    print("Initializing ChatGoogleGenerativeAI with gemini-2.0-flash-001...")
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-001", google_api_key=api_key
        )
        print("Invoking model...")
        result = await llm.ainvoke("Hello, is this model working?")
        print(f"Success! Response: {result.content}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(verify())
