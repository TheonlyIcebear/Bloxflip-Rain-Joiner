#!/usr/bin/env python -W ignore::DeprecationWarning

import cloudscraper, subprocess, pyautogui, threading, requests, logging, base64, json, time, os
from discord_webhook import DiscordWebhook, DiscordEmbed
from win10toast import ToastNotifier
from CaptchaBypass import Solver
from termcolor import cprint
from zipfile import *
from sys import exit


class main:
	def __init__(self):
		logging.basicConfig(filename="errors.txt", level=logging.DEBUG)
		self.crashPoints = None
		self.multiplier = 0
		self.version = "1.0.0"
		os.system("")
		try:
			self.getConfig()
			self.JoinRains()
		except KeyboardInterrupt:
			self.print("Exiting program.")
			exit()
		except Exception as e:
			open("errors.txt", "w+").close()
			now = time.localtime()
			logging.exception(f'A error has occured at {time.strftime("%H:%M:%S %I", now)}')
			self.print("An error has occured check logs.txt for more info", "error")
			time.sleep(2)
			raise
			exit()

	def print(self, message="", option=None): # print the ui's text with
		print("[ ", end="")
		if not option:
			cprint("AUTORAIN", "magenta", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "magenta")
		elif option == "error":
			cprint("ERROR", "red", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "red")
		elif option == "warning":
			cprint("WARNING", "yellow", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "yellow")
		elif option == "yellow":
			cprint("AUTORAIN", "yellow", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "yellow")
		elif option == "good":
			cprint("AUTORAIN", "green", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "green")
		elif option == "bad":
			cprint("AUTORAIN", "red", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "red")


	def sendwbmsg(self,url,message,title,color,content):
		if "https://" in url:
			data = {
				"content": content,
				"username": "Smart Bet",
				"embeds": [
									{
										"description" : message,
										"title" : title,
										"color" : color
									}
								]
			}
			r = requests.post(url, json=data)

	def clear(self): # Clear the console
		os.system('cls' if os.name == 'nt' else 'clear')


	def installDriver(self, version=None):
		uiprint = self.print
		if not version:
			uiprint("Installing newest chrome driver...", "warning")
			latest_version = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE").text
		else:
			uiprint(f"Installing version {version} chrome driver...", "warning")
			latest_version = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version}").text
		download = requests.get(f"https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_win32.zip")


		
		subprocess.call('taskkill /im "chromedriver.exe" /f')
		try:
			os.chmod('chromedriver.exe', 0o777)
			os.remove("chromedriver.exe")
		except:
			pass


		with open("chromedriver.zip", "wb") as zip:
			zip.write(download.content)


		with ZipFile("chromedriver.zip", "r") as zip:
			zip.extract("chromedriver.exe")
		os.remove("chromedriver.zip")
		uiprint("Chrome driver installed.", "good")




	def getConfig(self): # Get configuration from config.json file
		uiprint = self.print
		with open("config.json", "r+") as data:
			config = json.load(data)

			try:
				self.ping = config["webhook_ping"]
				self.webhook = DiscordWebhook(url=config["webhook"], content=self.ping)
				self.webhook_enabled = config["webhook_enabled"]
				self.notifications = config["notifications_enabled"]
				self.minimum_amount = float(config["minimum_amount"])
				self.autojoin = config["auto_join"]
				self.path = config["tesseract_path"]
				self.key = config["Serpapi_Api_Key"]
			except KeyError as k:
				uiprint(f"Invalid {k} key inside JSON file. Please redownload config from Gitub", "error")
				time.sleep(1.6)
				exit()


		print("[", end="")
		cprint(base64.b64decode(b'IENSRURJVFMg').decode('utf-8'), "cyan", end="")
		print("] ", end="")
		print(base64.b64decode(b'V2ViaG9vayBhbmQgTm90aWZjYXRpb24gY29kZSBieSBhbXByb2NvZGUgKGh0dHBzOi8vZ2l0aHViLmNvbS9hbXByb2NvZGUvQmxveGZsaXAtcmFpbi1ub3RpZmllcik=').decode('utf-8'))
		print("[", end="")
		cprint(base64.b64decode(b'IENSRURJVFMg').decode('utf-8'), "cyan", end="")
		print("] ", end="")
		print(base64.b64decode(b'QXV0byBKb2luZXIgYnkgSWNlIEJlYXIjMDE2Nw==').decode('utf-8'))
		time.sleep(3)
		self.clear()
			
		

	def CurrentRains(self):
		minimum_amount = self.minimum_amount
		uiprint = self.print
		sent = False
		


		while True:	
			try:
				scraper = cloudscraper.create_scraper()
				r = scraper.get('https://api.bloxflip.com/chat/history').json()
				check = r['rain']
				if check['active'] == True:
					getduration = check['duration']
					convert = (getduration/(1000*60))%60
					duration = (int(convert))
					waiting = (convert*60+10)
					grabprize = float(check['prize'])
					prize = (format(int(round(grabprize)),","))
					if float(grabprize) >= minimum_amount:
						yield check
					time.sleep(waiting)
			except Exception as e:
				uiprint(e, "error")
				time.sleep(30)
				pass
			time.sleep(30)


	def JoinRains(self):
		webhook_enabled = self.webhook_enabled
		notifications = self.notifications
		autojoin = self.autojoin
		webhook = self.webhook
		uiprint = self.print
		path = self.path
		key = self.path

		realclass = None
		uiprint("Program started. Press Ctrl + C to exit")
		


		for check in self.CurrentRains():
			grabprize = str(check['prize'])[:-2]
			prize = (format(int(grabprize),","))
			host = check['host']
			getduration = check['duration']
			convert = (getduration/(1000*60))%60
			duration = (int(convert))
			waiting = (convert*60+10)
			sent = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(int(time.time())))
			uiprint(f"Bloxflip Rain!", "green")
			uiprint(f"Rain amount: {prize} R$", "yellow")
			uiprint(f"Expiration: {duration} minutes", "yellow")
			uiprint(f"Host: {host}", "yellow")
			uiprint(f"Timestamp: {sent}", "yellow")
			if notifications: 
				ToastNotifier().show_toast("Bloxflip Rain!", f"Rain amount: {prize} R$\nExpiration: {duration} minutes\nHost: {host}\n\n", icon_path="assets/Bloxflip.ico", duration=10)

			userid = requests.get(f"https://api.roblox.com/users/get-by-username?username={host}").json()['Id']
			thumburl = (f"https://www.roblox.com/headshot-thumbnail/image?userId={userid}&height=50&width=50&format=png")
			if webhook_enabled:
				try:
					embed = DiscordEmbed(title=f"{host} is hosting a chat rain!", url="https://bloxflip.com", color=0xFFC800)
					embed.add_embed_field(name="Rain Amount", value=f"{prize} R$")
					embed.add_embed_field(name="Expiration", value=f"{duration} minutes")
					embed.add_embed_field(name="Host", value=f"[{host}](https://www.roblox.com/users/{userid}/profile)")
					embed.set_timestamp()
					embed.set_thumbnail(url=thumburl)
					webhook.add_embed(embed)
					webhook.execute()
					webhook.remove_embed(0)
				except:
					pass

			if autojoin:
				uiprint("Joining rain...")
				start = pyautogui.locateCenterOnScreen('assets/Join.png', confidence = 0.7)
				if not start:
					uiprint("Join rain button not found. Opening bloxflip now...", "warning")
					subprocess.call("start https://bloxflip.com",shell=True)
					time.sleep(3)
					start = pyautogui.locateCenterOnScreen('assets/Join.png', confidence = 0.7)
				if start:
					pyautogui.moveTo(*start,0.5)
					pyautogui.click()
					pyautogui.moveTo(700,700, 5)
					Solver(path, key)
					uiprint("Joined rain successfully!", "good")

				else:
					uiprint("Failed to locate button even after site opened.", "error")


if __name__ == "__main__":
	main()