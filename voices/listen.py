from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from os import getcwd

# Setting up Chrome options
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless=new")  # Remove this if you want to see the browser

# Manually set ChromeDriver path
chrome_driver_path = r"C:\Users\HP\Desktop\JARVIS 5.0\Driver\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)

# Setting up the Chrome driver once (so it doesn't reopen every time)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Opening the website for speech recognition
website = "https://allorizenproject1.netlify.app/"
driver.get(website)

def listen():
    try:
        start_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'startButton')))
        start_button.click()
        print("\nListening...")  

        # Wait for the output text
        output_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'output')))
        
        while True:
            output_text = output_element.text.strip()
            if output_text:  # If speech is detected, return it
                return output_text  

    except Exception as e:
        print("An error occurred in listen.py:", e)
        return None  

# No need to quit the driver here, keep it running for future commands
