#!/usr/bin/env python -W ignore::DeprecationWarning

import cloudscraper, subprocess, threading, selenium, requests, bloxflip, logging, base64, json, time, os
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
from selenium_stealth import stealth
from selenium import webdriver
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
			self.browser.close()
			exit()
		except Exception as e:
			open("errors.txt", "w+").close()
			now = time.localtime()
			logging.exception(f'A error has occured at {time.strftime("%H:%M:%S %I", now)}')
			self.print("An error has occured check logs.txt for more info", "error")
			time.sleep(2)
			raise
			self.browser.close()
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
				self.auth = config["authorization"]
			except:
				uiprint("Invalid authorization inside JSON file. Enter your new authorization from BloxFlip", "error")
				time.sleep(1.6)
				exit()


			try:
				self.ping = config["webhook_ping"]
			except:
				uiprint("Invalid ping inside JSON file. Must be valid string", "error")
				time.sleep(1.6)
				exit()



			try:
				self.webhook = DiscordWebhook(url=config["webhook"], content=self.ping)
			except:
				uiprint("Invalid webhook inside JSON file. Make sure you copied it correctly", "error")
				time.sleep(1.6)
				exit()


			try:
				self.webhook_enabled = config["webhook_enabled"]
			except:
				uiprint("Invalid webhook_enabled boolean inside JSON file. Must be true or false", "error")
				time.sleep(1.6)
				exit()

			try:
				self.notifications = config["notifications_enabled"]
			except:
				uiprint("Invalid notifications_enabled boolean inside JSON file. Must be true or false", "error")
				time.sleep(1.6)
				exit()

			try:
				self.minimum_amount = float(config["minimum_amount"])
			except:
				uiprint("Invalid minimum_amount boolean inside JSON file. Must a valid number", "error")
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

		self.installDriver()
		options = webdriver.ChromeOptions()
		options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
		options.add_argument('--disable-extensions')
		options.add_argument('--profile-directory=Default')
		options.add_argument("--disable-plugins-discovery")
		options.add_argument('--disable-blink-features=AutomationControlled')
		options.add_argument('--incognito')
		options.add_experimental_option("excludeSwitches", ["enable-automation", 'enable-logging'])
		options.add_experimental_option('useAutomationExtension', False)		
		service = Service('chromedriver.exe')
		try:
			self.browser = webdriver.Chrome(service=service, options=options)
		except selenium.common.exceptions.SessionNotCreatedException:
			try:
				self.installDriver(100)
			except:
				uiprint("Chromedriver version not compatible with current chrome version installed. Update your chrome to continue.", "error")
				uiprint("If your not sure how to update just uninstall then reinstall chrome", "yellow")
				time.sleep(5)
				exit()


		browser = self.browser
		time.sleep(5)
		browser.get("https://bloxflip.com/a/IceBear") # Open bloxflip
		browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
		try:
			browser.execute_script(f'''localStorage.setItem("_DO_NOT_SHARE_BLOXFLIP_TOKEN", "{self.auth}")''') # Login with authorization
			browser.execute_script(f'''window.location = "https://bloxflip.com/a/IceBear"''')
			time.sleep(1)
			browser.execute_script(f'''window.location = "https://bloxflip.com/crash"''')
		except:
			pass

		

	def CurrentRains(self):
		minimum_amount = self.minimum_amount
		browser = self.browser
		uiprint = self.print
		sent = False
		


		while True:	
			try:
				scraper = cloudscraper.create_scraper()
				r = scraper.get('https://rest-bf.blox.land/chat/history').json()
				check = r['rain']
				if check['active'] == True:
					getduration = check['duration']
					convert = (getduration/(1000*60))%60
					duration = (int(convert))
					waiting = (convert*60+10)
					grabprize = str(check['prize'])[:-2]
					prize = (format(int(grabprize),","))
					if float(prize.replace(',', "")) >= minimum_amount:
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
		browser = self.browser
		webhook = self.webhook
		uiprint = self.print

		realclass = None
		uiprint("Program started. Press Ctrl + C to exit")
		subprocess.call('start "" "https://discord.gg/MyCDzqF54p"')
		


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
				ToastNotifier().show_toast("Bloxflip Rain!", f"Rain amount: {prize} R$\nExpiration: {duration} minutes\nHost: {host}\n\n", icon_path="logo.ico", duration=10)

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
		try:
			browser.get("https://bloxflip.com/a/IceBear")
			browser.execute_script(f'''localStorage.setItem("_DO_NOT_SHARE_BLOXFLIP_TOKEN", "{self.auth}")''') # Login with authorization
			browser.execute_script(f'''window.location = "https://bloxflip.com/crash"''')
			time.sleep(3)
			browser.find_element(By.XPATH, "//span[contains(text(),'Join')]").click()
			time.sleep(10)
			browser.execute_script(f'''window.location = "https://bloxflip.com/crash"''')
			time.sleep(3)
			browser.find_element(By.XPATH, "//span[contains(text(),'Join')]").click()
			browser.quit()
		except Exception as e:
			uiprint(e, "error")


if __name__ == "__main__":
	main()
