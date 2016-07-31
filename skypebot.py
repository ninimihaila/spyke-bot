import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import config
from messages.generators.build_generators import build_markov

user_agent = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
)

driver = webdriver.Firefox()
driver.set_window_size(1024, 768)


def wait(secs, message=''):
    """Wait a number of secs and print progress"""
    print(message) if message else False
    countdown = secs
    while countdown > 0:
        time.sleep(1)
        print(countdown, ' seconds left')
        countdown -= 1


def login_to_skype(driver):
    driver.get('https://web.skype.com/')
    wait(7)
    driver.find_element_by_css_selector('#username').send_keys(config.SKYPE['username'])
    driver.find_element_by_css_selector('#password').send_keys(config.SKYPE['password'])
    driver.find_element_by_css_selector('#password').send_keys('\n')
    wait(7, 'waiting for skype to load...')
    # print console log messages
    # import json
    # messages = json.loads(list(driver.get_log('har'))[0]['message'])['log']['entries']
    # cookies = [m for m in messages if m['response']['cookies']!=[]]
    # if len(cookies)>0:
    #     print('cookies')
    # else:
    #     driver.save_screenshot('a.png')


def send_skype_message(driver, message):
    xpath = config.SKYPE['conversation_xpath'].format(config.SKYPE['conversation_title'])
    driver.find_element_by_xpath(xpath).click()
    time.sleep(5)
    # click on the last textarea
    driver.find_elements_by_css_selector('#textarea-bindings textarea')[-1].click()
    time.sleep(3)
    ActionChains(driver).send_keys(message).send_keys('\n').perform()
    time.sleep(3)


if __name__ == '__main__':
    driver.implicitly_wait(10)
    login_to_skype(driver)
    m = build_markov('', json_files=[])  # write the paths to your json files here
    send_skype_message(driver, m.generate(size=None))
    driver.close()