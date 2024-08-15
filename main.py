from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time


def start_browser():
#    firefox_options = Options()
#    firefox_options.add_argument("--headless")  # Открыть браузер в фоновом режиме
#    service = Service('C:/geckodriver/')  # Укажите путь к вашему GeckoDriver
#    browser = webdriver.Firefox(service=service, options=firefox_options)
    browser = webdriver.Firefox()
    return browser


def search_wikipedia(browser, query):
    browser.get('https://www.wikipedia.org/')
    search_box = browser.find_element(By.ID, 'searchInput')
    search_box.send_keys(query)
    search_box.submit()
    time.sleep(2)  # Подождать, пока страница загрузится


def print_paragraphs(browser):
    paragraphs = browser.find_elements(By.CSS_SELECTOR, 'p')
    for i, paragraph in enumerate(paragraphs):
        print(f"Параграф {i + 1}: {paragraph.text}\n")
        user_input = input("Нажмите Ввод для перелистывания или введите цифру 0 для вызова меню: ")
        if user_input.lower() == '0':
            break


def list_links(browser):
    links = browser.find_elements(By.CSS_SELECTOR, '#bodyContent a')
    link_map = {}
    for i, link in enumerate(links):
        href = link.get_attribute('href')
        if href and href.startswith('https://ru.wikipedia.org/wiki/'):
            print(f"{i + 1}: {link.text}")
            link_map[i + 1] = href
    return link_map


def main():
    browser = start_browser()
    try:
        while True:
            query = input("Введите поисковый запрос (или 'exit' для выхода): ")
            if query.lower() == 'exit':
                break

            search_wikipedia(browser, query)

            while True:
                print("\nВыберите действие:")
                print("1. Листать параграфы текущей статьи")
                print("2. Выбрать другую статью из списка")
                print("3. Выйти из программы")
                choice = input("Ваш выбор: ")

                if choice == '1':
                    print_paragraphs(browser)
                elif choice == '2':
                    links = list_links(browser)
                    link_choice = int(input("Введите номер статьи: "))
                    if link_choice in links:
                        browser.get(links[link_choice])
                    else:
                        print("Неправильный выбор, попробуйте еще раз.")
                elif choice == '3':
                    return
                else:
                    print("Неправильный выбор, попробуйте еще раз.")
    finally:
        browser.quit()


if __name__ == "__main__":
    main()
