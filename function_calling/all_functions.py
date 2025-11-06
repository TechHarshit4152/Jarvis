import asyncio
import pyautogui
import aiohttp
import requests
import json


class KeyboardFunction:
    def can_handle(self, task):
        return task.get("action") == "press_key"

    async def execute(self, task):
        keys = task.get("keys", [])
        for key in keys:
            pyautogui.hotkey(*key.split("+"))  # e.g. "ctrl+c" → hotkey("ctrl","c")
            print(f"Keyboard Function pressed: {key}")
            await asyncio.sleep(0.1)  # small delay between keys
        return f"Keyboard Function pressed {len(keys)} keys"




class APIFunction:
    def can_handle(self, task):
        return task.get("action") == "api_call"

    async def execute(self, task):
        url = task.get("api")
        headers = {"User-Agent": "JARVIS/1.0 (Personal Assistant)"}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                data = await response.text()
                try:
                    json_data = json.loads(data)
                    # Return only the 'extract' field for clean text
                    text = json_data.get("extract", "")
                    return text
                except json.JSONDecodeError:
                    return "❌ Failed to parse JSON from API"