from openai import OpenAI

def use_chatgpt():
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
       # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "What is the main challenge in ML ?"}
    ]
    )

    print(completion.choices[0].message)

    return completion.choices[0].message