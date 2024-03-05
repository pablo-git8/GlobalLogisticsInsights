# Imports
import os
import json
import time
import openai
import sqlite3
import pandas as pd

from datetime import datetime
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Load the variables from .env into the environment
load_dotenv()
variable = "No"

def initialize():
    # Write a sample text file to the current working directory
    sample_text = "This is a sample text for testing. 1"

    with open('sample.txt', 'w') as file:
        file.write(sample_text)

def call_func_var():
    return variable
