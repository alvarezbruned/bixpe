import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def is_in_page(selector):
    try:
        if "@" in selector:
            element = driver.find_element_by_xpath(selector)
        else:
            element = driver.find_element_by_css_selector(selector)
        return element
    except Exception:
        print(selector + ' Not found')
        return False


def active_action(action):
    start_button = 'button#btn-start-workday'
    stop_button = 'button#btn-stop-workday'
    lunch_button = 'button#btn-pause-lunch'
    come_back_from_lunch_button = 'button#btn-resume-workday'
    confirm_button = 'button.swal2-confirm.swal2-styled'
    switch = {
        'start' : start_button,
        'stop' : stop_button,
        'lunch' : lunch_button,
        'comBackFromLunch' : come_back_from_lunch_button
    }
    action_to_click = is_in_page(switch.get(action,'error'))
    if action_to_click:
        action_to_click.click()
    time.sleep(2)
    action_to_click = is_in_page(confirm_button)
    if action_to_click:
        action_to_click.click()


# driver = webdriver.Remote("firefox")
driver = webdriver.Firefox()

driver.get("https://auth2.bixpe.com/Account/Login")

driver.maximize_window()

username = is_in_page('input#Username')
if username:
    username.click()
    username.send_keys(os.getenv('USER_NAME', 'miuser'))

password = is_in_page('input#Password')
if password:
    password.click()
    password.send_keys(os.getenv('PASSWORD', 'mipass'))
    password.send_keys(Keys.ENTER)

time.sleep(5)

startActive = '.sl-item:nth-child(1) i.fa.fa-play.fa-2x.text-success'
stopActive = '.sl-item:nth-child(1) .fa.fa-stop.fa-2x.text-danger'
lunchActive = '.sl-item:nth-child(1) i.fa.fa-pause.fa-2x.text-warning'
comeBackFromLunchActive = '.sl-item:nth-child(1) i.fa.fa-refresh.fa-2x.text-success'
expectedStatus = os.getenv('STATUS', 'stop')
actualStatus = 'no'

driver.get('https://worktime.bixpe.com/')
time.sleep(3)


def actual_status():
    global actualStatus
    if is_in_page(startActive):
        actualStatus = 'start'
        print('status load ' + actualStatus)
    else:
        if is_in_page(stopActive):
            actualStatus = 'stop'
            print('status load ' + actualStatus)
        else:
            if is_in_page(lunchActive):
                actualStatus = 'lunch'
                print('status load ' + actualStatus)
            else:
                if is_in_page(comeBackFromLunchActive):
                    actualStatus = 'comBackFromLunch'
                    print('status load ' + actualStatus)
                else:
                    print('tenemos cambios en web')


actual_status()

if actualStatus == expectedStatus:
    print(actualStatus + ' nada que hacer')
else:
    active_action(expectedStatus)
    time.sleep(5)

actual_status()
if actualStatus == expectedStatus:
    print(actualStatus + ' nada que hacer')

driver.close()
