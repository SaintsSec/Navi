#!/bin/python3
"""
Name:        Navi | personality.py
Author:      Alex Kollar (https://github.com/AlexKollar/navi | @ssgcythes)
description: custom responses for navi's personality.     
"""
import os, sys, random, time

def lifelike():
    actions = [
        "Navi: *brushes hair behind her ear before adjusting glasses.*",
        "Navi: *Leans back in chair placing her hands behind her head with a sigh*",
        "Navi: *Goes to make a cup of tea. Returning a few moments later with a happy expression*"               
    ]
    for i in actions:
        time.sleep(30)
        action = random.choice(actions)
        print(action)

def sayings():
    comedy = [
        "The answer to life the universe and everything is 42"
    ]