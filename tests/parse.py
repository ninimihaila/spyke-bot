from messages.parsehistory.messageparse import parse_message
import unittest

class TestParsing(unittest.TestCase):
    def test_parse_message(self):
        messages = [
            "\n      uite-i pe toti ba <span class=\"emoticon laugh\" title=\"Laugh :D\">:D</span>\n    ",
            "\n      what's uup??\n    ",
            "\n      care produce ce ? bataturi si ciarcane ? <span class=\"emoticon smile\" title=\"Smile :)\">:)</span>)\n    ",
            "\n      <span class=\"emoticon smile\" title=\"Smile :)\">:)</span>)\n    ",
            "\n      (ref video : <a href=\"http://youtu.be/U8Y3e1c9RMg\" target=\"_blank\">http://youtu.be/U8Y3e1c9RMg</a> )\n    ",
            "\n      <a href=\"http://i.imgur.com/rnE90.gif\" target=\"_blank\">http://i.imgur.com/rnE90.gif</a>\n    ",
            '\n      in ce mai <span class=\"emoticon speechless\" title=\"Speechless :|\">:|</span> <span class="emoticon eg" title="Evil ]:)">&gt;:)</span>\n    ',
            "\n      you can\\'t  ---&gt; <br>\n    ",
        ]
        expected = [
            "uite-i pe toti ba :D",
            "what's uup??",
            "care produce ce ? bataturi si ciarcane ? :))",
            ":))",
            "(ref video : http://youtu.be/U8Y3e1c9RMg )",
            "http://i.imgur.com/rnE90.gif",
            "in ce mai :| >:)",
            "you can't  ---> \n"
        ]
        for i in range(0, len(messages)):
            parsed = parse_message(messages[i])
            self.assertEqual(parsed, expected[i])


if __name__ == '__main__':
    unittest.main()