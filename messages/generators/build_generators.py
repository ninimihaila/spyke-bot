from messages.generators.markov import Markov
from messages.parsehistory.messageparse import load_messages, parse_message


def build_markov(author, json_files):
    messages = load_messages(json_files=json_files)
    markov = Markov()
    if author:
        messages = filter(lambda x: x['author'] == author, messages)
    for m in messages:
        markov.append_words(parse_message(m['message']))
    markov.analyze_text()
    return markov

