import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import config
import itertools
# import pickle
import random
import time
from messages.generators.build_generators import build_markov


def debug_signal_handler(signal, frame):
    import pudb;pu.db


import signal
signal.signal(signal.SIGINT, debug_signal_handler)


markov = build_markov(author='', json_files=[
    # write the paths to your json files here
])


def wait(secs, message='', silent=False):
    """Wait a number of secs and print progress"""
    print(message) if message else False
    countdown = secs
    while countdown > 0:
        time.sleep(1)
        if not silent:
            print(countdown, ' seconds left')
        countdown -= 1


def login_to_skype(driver):
    driver.get('https://web.skype.com/')
    wait(3)
    driver.find_element_by_css_selector('#username').send_keys(config.SKYPE['username'])
    driver.find_element_by_css_selector('#signIn').click()
    wait(3)
    driver.find_element_by_css_selector('.placeholder').click()
    driver.find_element_by_css_selector('.placeholder').send_keys(config.SKYPE['password'])
    driver.find_element_by_css_selector('.btn-primary').click()
    wait(10, 'waiting for skype to load...')

    # print console log messages
    # import json
    # messages = json.loads(list(driver.get_log('har'))[0]['message'])['log']['entries']
    # cookies = [m for m in messages if m['response']['cookies']!=[]]
    # if len(cookies)>0:
    #     print('cookies')
    # else:
    #     driver.save_screenshot('a.png')


def send_skype_message(driver, message):
    if not message:
        return

    xpath = config.SKYPE['conversation_xpath'].format(config.SKYPE['conversation_title'])
    driver.find_element_by_xpath(xpath).click()

    # click on the last textarea
    chat_area = driver.find_element_by_css_selector('#chatInputAreaWithQuotes')
    chat_area.click()
    chat_area.send_keys(message)
    chat_area.send_keys('\n')

    driver.find_element_by_css_selector('.send-button').click()


def word_after(line, word):
    if word in line:
        position = line.index(word) + len(word)
        after = ''.join(itertools.takewhile(lambda x: x != ' ', line[position:]))
    else:
        after = None
    return after


reply_dict = {
    # for example: "spykebot, say something about python"
    # would make it generate a sentence starting with "python"
    'say something': {
        'reply': markov.generate,
        'param': lambda l: {'seed': word_after(l, ' about ')},
    },
    'greet': {
        'reply': lambda: 'hello',
    },
    # add other custom commands and replies here
}


def process_message(message):
    for key in reply_dict:
        if key.lower() in message['message'].lower():
            command = reply_dict[key]
            param = command['param']
            if param:
                reply = command['reply'](**param(message['message']))
            else:
                reply = command['reply']()
            return reply


if __name__ == '__main__':
    driver = webdriver.Firefox()  # change if you need to use chrome
    driver.set_window_size(1024, 768)
    driver.implicitly_wait(10)
    login_to_skype(driver)
    send_skype_message(driver, random.choice(['hello', 'hi']))
    handled = set()
    number_of_messages = 5
    print('Begin listening for messages')
    listening = False
    while True:
        wait(3)
        if random.randint(0, 500) < 1:
            message = markov.generate()
            print('sending message: ', message)
            send_skype_message(driver, markov.generate())
            continue

        try:
            last_messages = []
            for message in driver.find_elements_by_css_selector('.content')[-number_of_messages:]:
                processed_message = {}
                name_els = message.find_elements_by_xpath('..//a')
                name = name_els[0].get_attribute('textContent').strip() if name_els else 'self'
                processed_message['name'] = name
                processed_message['message'] = message.get_attribute('textContent').strip()
                msg_time = (
                    message.find_element_by_xpath('..//div[contains(@class, "timestamp")]')
                    .get_attribute('textContent')
                    .strip()[-8:]
                )
                processed_message['time'] = msg_time
                processed_message['id'] = message.get_attribute('id')[4:]
                last_messages.append(processed_message)

            # import pudb;pu.db
            for message in last_messages:
                if message['id'] not in handled and config.SKYPE['callname'] in message['message'].lower():
                    print(message['name'], 'asked', message['message'], 'at', message['time'])
                    handled.add(message['id'])
                    reply = process_message(message)
                    send_skype_message(driver, reply)
                    print('sent reply:', reply)
        except Exception as ex:
            import pudb;pu.db
            print('An error occured: ', ex)

    driver.close()
