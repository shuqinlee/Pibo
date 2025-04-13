import groq
import dotenv
import os

dotenv.load_dotenv()

client = groq.Groq(api_key=os.getenv("groq_api_key"))

def t2t(history, prompt):
    messages = history
    messages.append({"role": "user", "content": f"{prompt} 用中文回答 长度适合语音对话 casual一点"})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    response_text = response.choices[0].message.content
    return response_text

def multiturn_text2text():
    history = []
    while True:
        prompt = input("You: ")
        response = t2t(history, prompt)
        history.append({"role": "assistant", "content": response})
        print(f"Assistant: {response}")
        history.append({"role": "user", "content": response})
        

if __name__ == "__main__":
    multiturn_text2text()