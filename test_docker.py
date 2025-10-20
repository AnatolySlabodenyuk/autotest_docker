import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SELENIUM_HOST = os.getenv("SELENIUM_HOST", "localhost")
REMOTE_URL = f"http://{SELENIUM_HOST}:4444"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def test_duckduckgo_search_results():
    # driver = webdriver.Chrome()  # локальный браузер

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor=REMOTE_URL,  # "http://localhost:4444",
        options=options
    )

    try:
        driver.get("https://duckduckgo.com/")
        # Найти поле поиска на главной странице
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchbox_input"))
        )
        search_input.send_keys("Нетология")
        search_input.send_keys(Keys.RETURN)

        # Ждать появления результатов поиска
        WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-nrn='result']"))
        )

        # Получить все результаты поиска
        results = driver.find_elements(By.CSS_SELECTOR, "article[data-nrn='result']")
        logger.info(f"Найдено результатов: {len(results)}")
        assert len(results) > 0, "Результаты не найдены"

    finally:
        input('Нажмите что-нибудь\n')
        driver.quit()


if __name__ == "__main__":
    test_duckduckgo_search_results()
