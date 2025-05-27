import google.generativeai as genai

genai.configure(api_key="AIzaSyC8YlNjae83qnN8vD5mZUZFAqcgOUwVIqo")

model = genai.GenerativeModel("models/gemini-2.5-pro-preview-05-06")
chat = model.start_chat()

print("Healthcare Assistant Chatbot (type 'exit' to quit)\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye.")
        break

    prompt = (
        "You are a professional medical assistant.\n"
        "Provide concise, factual answers in the same language as the user's question.\n"
        "Do NOT provide diagnoses or prescriptions.\n"
        "Advise users to consult healthcare professionals for medical concerns.\n"
        f"Question: {user_input}\nAnswer:"
    )

    response = chat.send_message(prompt)
    print("Assistant:", response.text.strip())
