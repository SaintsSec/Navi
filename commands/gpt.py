import openai
from mods import mods

openai.api_key = "ENTER YOUR KEY HERE"

command = "/gpt"
use = "Access GPT"
art = mods.gptArt

def generate_completion(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7
    )
    if response.choices:
        return response.choices[0].text.strip()
    return ""

def run():
    print(art)
    prompt = input("Navi> [!] - Enter your prompt \n=> ")
    completion = generate_completion(prompt)
    print("Navi> ")
    print(completion)

if __name__ == "__main__":
    run()
