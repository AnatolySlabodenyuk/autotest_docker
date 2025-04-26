import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# если контейнер на этой же машине
SELENIUM_HOST = os.getenv("SELENIUM_HOST", "localhost")
SELENIUM_PORT = os.getenv("SELENIUM_PORT", "4444")

# Указываем удалённый WebDriver
driver = webdriver.Remote(
    command_executor=f"http://{SELENIUM_HOST}:{SELENIUM_PORT}",
    options=webdriver.ChromeOptions()
)

try:
    # Переходим на сайт duckduckgo
    driver.get("https://duckduckgo.com")

    wait = WebDriverWait(driver, 10)  # Даем странице загрузиться

    # Находим поле поиска
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))

    # Вводим запрос
    search_query = "Selenium Python"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    # Ждем загрузки результатов
    wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "a.result__a")))
    results = driver.find_elements(By.CSS_SELECTOR, "a.result__a")

    if results:
        print(f"Найдено результатов: {len(results)}")
    else:
        print("Результаты поиска не найдены.")

except Exception as e:
    driver.save_screenshot("error.png")
    print(f"Произошла ошибка: {e}")

# Сессия будет активна до тех пор, пока не нажать Enter
finally:
    input("Тест запущен. Нажмите Enter, чтобы завершить и закрыть сессию...")
    driver.quit()
