# SPyke Bot

Create skype bots easily


### What's this? ###

Spyke Bot is a collection of scripts that can be used
to make skype bots


### How does it work? ###

The scripts consist of multiple services:
- [optional] a script to scrape the skype history of a conversation
- a selenium script to connect to the web version of skype
to send and receive messages


### Installing ###

* `cd` to a folder of your choosing
* `git clone <project>`
* `cd <project dir>/`
* `virtualenv -p <path-to-python3> venv`
* (linux) `source venv/bin/activate`
* `pip install -r requirements.txt`
* `cp config_example.py config.py`
* update the `config.py` file to suit your needs

### (Optional) getting the skype history ###

* use skyperious to export the history of a conversation to 
html
* use the javascript helper in `messages/parsehistory` to scrape
the html:
    - open the exported html file in chrome (may take a while)
    - open chrome dev tools (press F12)
    - copy paste the contents of the script in the console and hit enter
    - it will ask you to save a .json file with the results
* after this, store the file in `messages/results` and use the generator
to create a new text from the history
