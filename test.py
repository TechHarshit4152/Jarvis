# main.py
import asyncio
from function_calling.all_functions import KeyboardFunction, APIFunction
from function_calling.function_hub import Hub

# 1. Create Hub
hub = Hub()

# 2. Create limbs
keyboard = KeyboardFunction()
api = APIFunction()

# 3. Register limbs
hub.register_function(keyboard)
hub.register_function(api)

# 4. Push tasks
hub.push_task({
    "action": "press_key",
    "keys": ["win+e"]
})

hub.push_task({
    "action": "api_call",
    "api": "https://en.wikipedia.org/api/rest_v1/page/summary/Quantum_entanglement"
})

# 5. Run hub
asyncio.run(hub.run())
