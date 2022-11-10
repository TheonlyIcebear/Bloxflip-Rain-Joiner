# Bloxflip Auto Rain Joiner 🤖

A simple program that will bypass [bloxflip's](https://bloxflip.com) chat captcha system allowing the program to automatically collect the robux from rains

# Usage ⚙
The config.json file should look like
```json
{
	"minimum_amount": 500,
	"auto_join": true,
	"webhook_enabled": true,
	"webhook": "https://discord.com/api/webhooks/xxxxxxxxxxx/xxxxxxxxxxxxxxxxxxxxx",
	"webhook_ping": "<@1234567890>",
	"notifications_enabled": true,
	"tesseract_path": "C:\\Users\\USER\\AppData\\Local\\Tesseract-OCR\\tesseract",
	"Serpapi_Api_Key": ""
}
```

### minimum_amount:
Minimum rain amount intended for the program required to send you a notification. If you dont want this and want to be notified of all rains leave it at 500

Example: If you set it to 1000 it will only notify you of rains that are bigger then or equal to 1000 R$


### notifications_enabled:
If set to "true" then a popup on the bottom right on your screen will display showing you information about the current rain

Here is an example:

![unknown (2)](https://user-images.githubusercontent.com/79641603/161392482-74abad64-d724-466a-8c7a-2f6d87acf3c6.png)

### webhook_enabled:
Should be obvious but if you want the rain notifier to send a message to your discord webhook set it to "True"

### webhook_ping:
You can now ping a role or user instead of @everyone. If you need help getting an ID im sure this will help:

https://youtu.be/KVLdpboY7bg

Setting up ping:

If you want to ping **@everyone** or **@here** make sure your webhook_ping setting looks something like this:
```
"webhook_ping": "@everyone",
```
If you want to ping a **user** make sure your webhook_ping setting looks something like this:
```
"webhook_ping": "<@747719812054253568>",
```
If you want to ping a **role** just put a **&** symbol infront of the numbers. It should look something like this:
```
"webhook_ping": "<@&690632567663575090>",
```

**Obviously these are examples, replace the numbers with your own**

### webhook:
If you set webhook_enabled to "True" input your webhook into here to it can actually send it to you

Example of webhook:

![image](https://user-images.githubusercontent.com/79641603/161392598-616dda5d-adb5-4ff4-9b60-d46ea8581128.png)
