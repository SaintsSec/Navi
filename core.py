#!/bin/python3
"""
Name:        Navi | core.py
Author:      Alex Kollar (https://github.com/AlexKollar/navi | @ssgcythes)
description: Navi is a conversational AI built to be a personal assistant for cyber security.     
"""
from transformers import AutoTokenizer, AutoModelForCausalLM
from os import system
from modules import personality
from modules import menus
import torch, os, sys

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
print(menus.banner)
# personality.lifelike()
for steps in range(sys.maxsize**10):
    text = input(">> ")
    # if text == "help" or "-h":
    #     print("Navi: Maybe this will help you\n")
    #     print(menus.bothelp)
    # if text == "cls" or "clear":
    #     system('clear')
    # if text == "reset" or "reboot":
    #     print(f"Navi: Rebooting... lets try again :D")
    #     os.execl(sys.executable, sys.executable, *sys.argv)
    # if text == "goodbye" or "Goodbye" or "See you later":
    #     print("Navi: Thank you for talking me! I look forward to seeing you again!")
    #     exit()
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