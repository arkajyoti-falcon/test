import os, time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title="Selenium + Streamlit", layout="centered")
st.title("Selenium → open a page and copy content")

url = st.text_input("Web address", "https://www.google.com")
css = st.text_input("CSS selector to extract (optional)", "h1")
headless = st.checkbox("Run headless (required on Streamlit Cloud)", value=True)

if st.button("Open & fetch"):
    driver = None
    try:
        opts = Options()

        # Use system Chromium if present (Streamlit Cloud)
        for p in ("/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome"):
            if os.path.exists(p):
                opts.binary_location = p
                break

        if headless:
            opts.add_argument("--headless=new")
        # Your original flags (fixed the typo)
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--window-size=1920,1080")

        # Prefer system chromedriver on cloud; fallback to webdriver-manager locally
        service = Service("/usr/bin/chromedriver") if os.path.exists("/usr/bin/chromedriver") \
                 else Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=opts)

        with st.spinner(f"Opening {url} …"):
            driver.get(url)
            time.sleep(1)

        st.success("Page opened.")
        st.write("**Title:**", driver.title)

        if css.strip():
            try:
                text = driver.find_element(By.CSS_SELECTOR, css).text.strip()
                st.write("**Extracted text:**", text or "(empty)")
            except Exception as e:
                st.warning(f"Couldn’t find `{css}`: {e}")

    except Exception as e:
        st.error(f"WebDriver error: {e}")
    finally:
        try:
            if driver:
                driver.quit()
        except:
            pass
