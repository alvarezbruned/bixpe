import os
import time
import logging
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

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


def is_correct_status(status_option):
    is_correct = False
    status_mapping = {
        'Start': True,
        'Stop': True,
        'Pause': True,
        'Resume': True
    }
    is_correct = status_mapping.get(status_option)
    return is_correct


def actual_status():
    global actualStatus
    startActive = '.sl-item:nth-child(1) i.fa.fa-play.fa-2x.text-success'
    stopActive = '.sl-item:nth-child(1) .fa.fa-stop.fa-2x.text-danger'
    pauseActive = '.sl-item:nth-child(1) i.fa.fa-pause.fa-2x.text-warning'
    resumeActive = '.sl-item:nth-child(1) i.fa.fa-refresh.fa-2x.text-success'
    actualStatus = 'no'
    if is_in_page(startActive):
        actualStatus = 'Start'
        print('status load ' + actualStatus)
    else:
        if is_in_page(stopActive):
            actualStatus = 'Stop'
            print('status load ' + actualStatus)
        else:
            if is_in_page(pauseActive):
                actualStatus = 'Pause'
                print('status load ' + actualStatus)
            else:
                if is_in_page(resumeActive):
                    actualStatus = 'Resume'
                    print('status load ' + actualStatus)
                else:
                    print('tenemos cambios en web')


def chrome_webdriver():
    global driver
    try:
        driver = webdriver.Chrome(executable_path=r"/usr/lib/chromium-browser/chromedriver")
    except Exception as e:
        try:
            driver = webdriver.Chrome(executable_path=r"./chromedriver76")
        except Exception as e2:
            try:
                driver = webdriver.Chrome(executable_path=r"./chromedriver77")
            except Exception as e3:
                try:
                    driver = webdriver.Chrome(executable_path=r"./chromedriver83")
                except Exception as e4:
                    print('version chromedriver fails')
    return driver


os.environ['DISPLAY'] = os.getenv('INS_DISPLAY', ':0.0')
logging.basicConfig(level=logging.INFO)
# driver = webdriver.Firefox(executable_path=r"./geckodriver")
driver = chrome_webdriver()

driver.get("https://auth2.bixpe.com/Account/Login")

driver.maximize_window()

type_if_exist('input#Username', os.getenv('BIXPE_USER', 'miuser'))
type_if_exist('input#Password', os.getenv('BIXPE_PASS', 'mipass'))
type_if_exist('input#Password', Keys.ENTER)


expectedStatus = os.getenv('BIXPE_STATUS', 'start').capitalize()

actual_status()

if actualStatus != expectedStatus:
    if is_correct_status(expectedStatus):
        time.sleep(8)
        driver.get("https://worktime.bixpe.com/WorkDay/" + expectedStatus)
        time.sleep(8)
        driver.get("https://worktime.bixpe.com/")
        time.sleep(8)
    else:
        print('status is not valid')

actual_status()

if actualStatus == expectedStatus:
    print(actualStatus + ' it\'s actual status')


time.sleep(2)

driver.close()
