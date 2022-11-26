import random

def idk():
    idkList = [
        "I am not sure how to respond.",
        "Oh! It appears you wrote something I dont understand yet.",
        "Do you mind rephrasing that for me? I am still learning",
        "I'm terribly sorry, I didn't quite catch that..."
    ]
    listCount = len(idkList)
    idkItem = random.randrange(listCount)
    return idkList[idkItem]


