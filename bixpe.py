import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def is_in_page(selector):
    try:
        if "@" in selector:
            return driver.find_element_by_xpath(selector)
        return driver.find_element_by_css_selector(selector)
    except Exception:
        print(selector + ' Not found')
        return False


def click_if_exist(path_locator):
    element = is_in_page(path_locator)
    if element:
        element.click()
        return element
    return False


def type_if_exist(path_locator, keys_to_send):
    element = click_if_exist(path_locator)
    if element:
        element.send_keys(keys_to_send)


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
    click_if_exist(switch.get(action, 'error'))
    time.sleep(2)
    click_if_exist(confirm_button)


def actual_status():
    global actualStatus
    startActive = '.sl-item:nth-child(1) i.fa.fa-play.fa-2x.text-success'
    stopActive = '.sl-item:nth-child(1) .fa.fa-stop.fa-2x.text-danger'
    lunchActive = '.sl-item:nth-child(1) i.fa.fa-pause.fa-2x.text-warning'
    comeBackFromLunchActive = '.sl-item:nth-child(1) i.fa.fa-refresh.fa-2x.text-success'
    actualStatus = 'no'
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





driver = webdriver.Firefox(executable_path=r"./geckodriver")

# driver.get("https://auth2.bixpe.com/Account/Login")
# user = 'bixpe-cookies'
# try:
#     cookies = pickle.load(open("./" + user + ".pkl", "rb"))
#     for cookie in cookies:
#         # if 'expiry' in cookie:
#         #     del cookie['expiry']
#         driver.add_cookie(cookie)
# except Exception as e:
#     print('no hay cookies' + str(e))

driver.get("https://auth2.bixpe.com/Account/Login")
driver.maximize_window()

type_if_exist('input#Username', os.getenv('BIXPE_USER', 'miuser'))
type_if_exist('input#Password', os.getenv('BIXPE_PASS', 'mipass'))
type_if_exist('input#Password', Keys.ENTER)

time.sleep(8)

expectedStatus = os.getenv('BIXPE_STATUS', 'stop')
actual_status()

if actualStatus == expectedStatus:
    print(actualStatus + ' nada que hacer')
else:
    active_action(expectedStatus)
    time.sleep(5)
    actual_status()
    if actualStatus == expectedStatus:
        print(actualStatus + ' nada que hacer')

pickle.dump( driver.get_cookies(), open("./" + user + ".pkl","wb"))
time.sleep(2)

driver.close()
driver.quit()

