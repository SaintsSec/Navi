from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from os import system
from modules import menus
import os 
import sys

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
print(menus.banner)
for steps in range(sys.maxsize**10):
    text = input(">> ")
    if text == "help":
        print("Navi: Maybe this will help you\n")
        print(menus.bothelp)
    if text == "cls":
        system('clear')
    if text == "reset":
        print(f"Navi: I am sorry I let you down, lets try again :D")
        os.execl(sys.executable, sys.executable, *sys.argv)
    if text == "exit":
        print("Navi: Thank you for talking me! I look forward to seeing you again!")
        exit()
    else:
        input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
        bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if steps > 0 else input_ids
        # generate a bot response
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
        )
        #print the output
        output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"Navi: {output}")