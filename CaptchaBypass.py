import cloudscraper, pytesseract, subprocess, pyautogui, threading, requests, logging, base64, nltk, json, time, re, io, os
from discord_webhook import DiscordWebhook, DiscordEmbed
from win10toast import ToastNotifier
from serpapi import GoogleSearch
from termcolor import cprint
from tqdm import tqdm
from tkinter import *
from zipfile import *
from sys import exit
from PIL import *


class Solver:
    def __init__(self, path, key):
        self.blacklist = [
            "umber",
        ]
        self.key = key
        self.done = False
        self.setup(path.replace('\\', '\\\\'))
        self.solve()

    def goTo(self, x=None, y=None, filename=None, wait=0.005):
        if filename:
            start = pyautogui.locateCenterOnScreen(filename, confidence = 0.7)
            print(*start)
            pyautogui.moveTo(*start,wait)

        else:
            pyautogui.moveTo(x,y, wait)

    def setup(self, path):
        with open(f"{os.environ['LOCALAPPDATA']}\\Programs\\Python\\Python310\\lib\\site-packages\\pytesseract\\pytesseract.py", "r+") as package:
            data = package.read().replace("tesseract_cmd = 'tesseract'", f"tesseract_cmd = '{path}' ")
        with open(f"{os.environ['LOCALAPPDATA']}\\Programs\\Python\\Python310\\lib\\site-packages\\pytesseract\\pytesseract.py", "w+") as package:
            package.write(data)

        pytesseract.tesseract_cmd = f"{os.environ['LOCALAPPDATA']}\\Tesseract-OCR\\tesseract"

    def keepAlive(self):
        goTo = self.goTo
        time.sleep(30)
        while not self.done:
            start = pyautogui.position()
            loc = pyautogui.locateCenterOnScreen('assets/Anchor.png', confidence = 0.7)
            if not loc:
                break

            goTo(*loc, wait=0)
            pyautogui.click()
            goTo(*start, wait=0)
            time.sleep(30)

    def click(self, pos):
        self.goTo(pos[0]+60, pos[1]+60)
        pyautogui.click()

    def solve(self):
        goTo = self.goTo
        click = self.click
        goTo(filename='assets/Captcha.png')
        scraper = cloudscraper.create_scraper()
        pyautogui.click()
        time.sleep(2)
        while not pyautogui.locateCenterOnScreen('assets/Anchor.png', confidence = 0.7):
            print("Waiting for captcha to load...")
        threading.Thread(target=self.keepAlive).start()
        while pyautogui.locateCenterOnScreen('assets/Anchor.png', confidence = 0.7):
            goTo(filename='assets/Anchor.png')
            pyautogui.click()
            loc = pyautogui.position()

            imgtop = loc.y-84
            imgbottom = loc.y-10
            imgleft = loc.x-96
            imgright = loc.x+164

            size = 120
            divider = 10
            top = loc.y+28
            bottom = loc.y-10
            left = loc.x-96
            right = loc.x+154

            width = abs(imgright-imgleft)
            height = abs(imgtop-imgbottom)
            query = pyautogui.screenshot(region=(imgleft,imgtop, width, height))
            query.save("assets/query.png", format='PNG')
            query = Image.open("assets/query.png")
            tags = [*"NJVR"]
            
            objectives = pytesseract.image_to_string(query)[:-1].replace("\n", "").split(" ")[5:]
            objectives = [word[0] for word in nltk.pos_tag(objectives) if word[1][0] in tags]


            imagesPosition = []
            for x in list(range(9)):
                row = x % 3
                column = x // 3
                imagesPosition.append([left+(row*size)+(divider*row), top+(column*size)+(divider*column)])
            


            for count, pos in enumerate(imagesPosition):
                img = pyautogui.screenshot(region=(pos[0],pos[1], 120, 120))
                img = img.crop()

                img.save("assets/screenshot.png", format='PNG')
                

                multipart = {'file': ('screenshot.png', open('assets/screenshot.png', 'rb'))}
                file_link = requests.post("https://api.anonfiles.com/upload",files=multipart).json()["data"]["file"]["url"]["short"]
                id = file_link.split("/")[3]
                page = scraper.get(file_link).text
                index = page.index(f".anonfiles.com/{id}/")
                download_link = page[index-15:index+75].replace('"', '')
                params = {
                    "engine": "google_reverse_image",
                    "image_url": download_link,
                    "api_key": self.key
                }
                search = GoogleSearch(params)
                data = str([site["source"] for site in search.get_dict()["inline_images"]])
                print([[word, data[data.index(word)-1], data[data.index(word)+len(word)], len(word), data.count(word)] for word in objectives if word in data])
                print([(data.count(word) > 1) and (not ((data[data.index(word)-1].isalpha() or data[data.index(word)+len(word)].isalpha()) and (len(word) < 5))) for word in objectives])
                if all([(data.count(word) > 1) and (not ((data[data.index(word)-1].isalpha() or data[data.index(word)+len(word)].isalpha()) and (len(word) < 5))) for word in objectives]):
                    print("Clicking: ", count+1)
                    click(pos)
                            


            goTo(filename="assets/Done.png")
            pyautogui.click()
            for _ in range(2):
                click(pos[0])
                click(pos[1])
                print(1)
            


Solver("C:\\Users\\ekila\\AppData\\Local\\Tesseract-OCR\\tesseract", "add2b65cec22b18f1d077fe85fdaae1ba016bfa8a85a82ca9095bc14d9694fec")