from bs4 import BeautifulSoup
import requests
import csv
import sys
from os.path import exists


if len(sys.argv) > 1:
    if str(sys.argv[1]) == "give_hist":
        if exists("hist.csv"):
            with open("hist.csv","r") as file:
                reader = csv.reader(file,delimiter=' ')
                for row in reader:
                    print(" : ".join(row))
        sys.exit()

    word = str(sys.argv[1])
    page_to_scrape = requests.get("http://www.urbandictionary.com/define.php?term={}".format(word))
    soup = BeautifulSoup(page_to_scrape.content, "html.parser")
#quotes = soup.findAll("span", attrs={"class":"text"})
#authors = soup.findAll("small", attrs={"class":"author"})

    definition = soup.find("div", attrs={"class":"meaning"}).text

    print(word,":",definition)


    if len(sys.argv) > 2:
        if exists("hist.csv"):
            with open("hist.csv","a") as file:
                writer = csv.writer(file)
                writer.writerow([word, definition])
        else:
            with open("hist.csv","w") as file:
                writer = csv.writer(file)
                writer.writerow(["WORD","DEF"])
                writer.writerow([word,definition])
else:
    print("Invalid input: no argument given.")
    sys.exit()
#writer.writerow(["QUOTES", "AUTHORS"])

#for quote, author in zip(quotes,authors):
    #print(quote.text + " - " + author.text)
    #writer.writerow([quote.text, author.text])

#file.close()
