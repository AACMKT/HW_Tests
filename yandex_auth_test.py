from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

yandex_mail = 'INPUT_YOUR_MAIL_HERE@yandex.ru'
yandex_password = 'INPUT_YOUR_YANDEX_ACCOUNT_PASSWORD_HERE'


def test_yandex_auth():
    browser = webdriver.Chrome()
    browser.implicitly_wait(2)
    browser.get('https://dzen.ru/')
    browser.find_element(By.CLASS_NAME, 'login-button__textButton-3Y').click()
    try:
        browser.find_element(By.LINK_TEXT, 'Войти через Яндекс ID').click()
    except NoSuchElementException:
        browser.get('https://passport.yandex.ru/auth/')

    browser.find_element(By.ID, 'passp-field-login').send_keys(yandex_mail)
    browser.find_element(By.ID, 'passp:sign-in').click()
    browser.find_element(By.ID, 'passp-field-passwd').send_keys(yandex_password)
    browser.find_element(By.ID, 'passp:sign-in').click()
    browser.quit()
