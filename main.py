import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

st.set_page_config(page_title="Selenium + Streamlit (Non-Headless)", layout="centered")
st.title("Selenium → Fetch content (non-headless)")

url = st.text_input("Web address", "https://example.com")
css = st.text_input("CSS selector to extract", "h1")

if st.button("Fetch"):
    try:
        st.info("Launching Chrome (visible window)…")
        chrome_opts = Options()
        # Non-headless: do NOT add headless
        chrome_opts.add_argument("--start-maximized")
        chrome_opts.add_argument("--disable-infobars")
        chrome_opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_opts.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=chrome_opts)

        with st.spinner(f"Opening {url} …"):
            driver.get(url)
            # small wait for the page to render
            time.sleep(1.0)

        # Try to grab element text by CSS selector
        try:
            text = driver.find_element(By.CSS_SELECTOR, css).text.strip()
            st.success("Content fetched!")
            st.write("**Extracted text:**")
            st.write(text if text else "(Element found, but empty text)")
        except Exception as e:
            st.error(f"Couldn’t find element by selector `{css}`.\n{e}")

    except Exception as e:
        st.error(f"WebDriver error: {e}")
    finally:
        try:
            driver.quit()
        except Exception:
            pass
