import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import re
from state.state_types import State

### HELPER FUNCTIONS ###

def get_visible_text(url):
    options = Options()
    options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(2)  # Wait for the page to load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)

        html = driver.page_source
    finally:
        driver.quit()

    # Parse the HTML to get only visible text
    soup = BeautifulSoup(html, "html.parser")
    # You can filter out script and style elements, then get_text()
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    visible_text = soup.get_text(separator="\n", strip=True)

    return visible_text

def clean_text(text: str) -> str:
    # Replace newlines with space
    text = text.replace('\n', ' ')
    
    # Remove multiple spaces and strip leading/trailing spaces for each "section"
    # Split by 2+ spaces (assuming sections are separated by multiple spaces)
    sections = re.split(r'\s{2,}', text)
    sections = [section.strip() for section in sections]
    
    # Join sections back separated by single space
    clean_text = ' '.join(sections)
    
    # Remove non-English characters (keep English letters, digits, basic punctuation, whitespace)
    # This regex keeps a-z, A-Z, 0-9, common punctuation, and spaces
    clean_text = re.sub(r"[^a-zA-Z0-9\s\.,;:'\"?!()\-]", '', clean_text)
    
    # Optionally strip any leftover leading/trailing spaces
    return clean_text.strip()



### MAIN NODE FUNCTION ###
def get_page_content(state: State):
    page_text = get_visible_text(state['job_url'])   
    cleaned_text =  clean_text(page_text)

    return {"job_page_main_content": cleaned_text}