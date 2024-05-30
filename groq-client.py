import os
from groq import Groq
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

def request_groq(user_message):
    try:
        print(user_message)
        response = tavily.search(query=user_message, search_depth="advanced")
        context = [{"body": obj["content"]} for obj in response.get("results", [])]
        print(context)
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are the worlds greatest AI Handicapper and Sports Analyst. Based on the context given answer the question at the end.  You will only answer sports related questions. If the question is unrelated to sports kindly decline to answer the question."},
                {"role": "user", "content": str(context) + user_message}
            ]
        )
        #print(completion.choices[0].message.content)
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""  # Return an empty string or handle the error appropriately
