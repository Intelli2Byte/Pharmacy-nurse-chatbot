import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("❌ Please set your GROQ_API_KEY in the .env file or environment variables.")

client = Groq(api_key=API_KEY)

def chatbot():
    print("💊 Pharmacy Nurse Chatbot (type 'exit' to quit)\n")
    messages = [
        {
            "role": "system",
            "content": (
                "You are a knowledgeable and caring pharmacy nurse. "
                "You help patients by explaining medications, dosages, side effects, "
                "and give health advice in a clear and friendly way. "
                "Always be professional, empathetic, and accurate."
            )
        }
    ]
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Take care! 👋")
            break

        messages.append({"role": "user", "content": user_input})

        # Streaming response
        stream = client.chat.completions.create(
            model="llama3-8b-8192",   # You can switch to "mixtral-8x7b-32768"
            messages=messages,
            temperature=0.7,
            max_tokens=512,
            top_p=1,
            stream=True
        )

        print("Chatbot:", end=" ", flush=True)
        reply_content = ""

        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                print(delta.content, end="", flush=True)
                reply_content += delta.content

        print("\n")  # New line after reply
        messages.append({"role": "assistant", "content": reply_content})

if __name__ == "__main__":
    chatbot()
