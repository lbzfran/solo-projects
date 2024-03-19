from bs4 import BeautifulSoup
import requests
import csv
import sys
from os.path import exists

def get_words(single = False):

    words = []

    while True:
    
        word = input("Enter word to define-> ")
        if not word:
            words.append(None)
            break
        words.append(word)
        word = ''
        if single:
            break

    return words

def scrape(count: int, words: list) -> dict:

    wordDict = {}

    for idx in range(count):

        if not words[idx]:
            # skip None words.
            continue

        word = str(words[idx])
        
        page_to_scrape = requests.get("http://www.urbandictionary.com/define.php?term={}".format(word))

        soup = BeautifulSoup(page_to_scrape.content, "html.parser")
        
        wordInDB = soup.find("div", attrs={"class":"meaning"})

        if wordInDB:
            wordDict[word] = wordInDB.text
        else:
            wordDict[word] = None

    return wordDict


if len(sys.argv) > 1:
    definitions = scrape(len(sys.argv), sys.argv)

    for word in definitions.keys():
        print(f"{word}: {definitions[word]}")

    sys.exit()
else:
    print("No arguments given.")
    sys.exit()

if __name__ == "__main__":
    
    print(f"Welcome to the Urban Scraper.")
    while True:
        user = input("Please select an option (exit with any other key):\n1. Define One\n2. Define Multiple\ninput-> ")
        match user:
            case "1":
                word = get_words(True)
                definition = scrape(1,word)
                print(f"{word[0]}: {definition[word[0]]}")
                
            case "2":
                words = get_words()
                definitions = scrape(len(words),words)

                for word in words:
                    if word:
                        print(f"{word}: {definitions[word]}")
            case _:
                break


