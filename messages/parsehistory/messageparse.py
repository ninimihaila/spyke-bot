import datetime
import re
import json


"""
This script takes the .json files produced by the javascript scraper and outputs a .txt file with the conversation
history
The parse functions are also helpful
"""

def parse_time(time_str):
    format = '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.strptime(time_str, format)


def parse_id(id_str):
    return int(id_str[len('message:'):])


def parse_message(message_str):
    # trim whitespace
    message_str = message_str[len('\n      '):-len('\n    ')]
    # remove emoticon spans
    message_str = re.sub(r'\<span class=\"[\w ]+\" title=\"[\w ]+[:()\/\w]+\"\>(?P<emoticon>[:()\/\w]+)+\<\/span\>',
                         r'\g<emoticon>',
                         message_str)
    # remove link a's
    message_str = re.sub(r'\<a href=\"[^"]+\" target=\"\w+\"\>(?P<link>[^<]+)\<\/a\>',
                         r'\g<link>',
                         message_str)
    return message_str


def load_messages(json_files):
    messages = []
    for filename in json_files:
        with open(filename, encoding='utf8') as f:
            m = json.loads(f.read())
            messages += m
    return messages


if __name__ == '__main__':
    """
    This is not technically used, but if you want a human readable .txt file of your conversation from the
    scraped json files, use this
    """
    messages = load_messages(json_files=[])  # write the paths to your json files here

    for m in messages:
        m['time'] = parse_time(m['time'])
        m['id'] = parse_id(m['id'])
        m['message'] = parse_message(m['message'])

    with open('res.txt', 'w+', encoding='utf8') as f:
        for m in messages:
            f.write('{} ({}) {}: {}\n'.format(m['id'], m['time'], m['author'], m['message']))