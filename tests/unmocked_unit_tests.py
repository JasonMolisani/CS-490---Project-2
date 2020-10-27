import unittest
import sys
sys.path.append('../') # Allow for imports to work when run from within test folder
sys.path.append('./')  # Allow for imports to work when run from within project2 folder
import bot

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_BOT_ID = 42

testBot = bot.Bot(KEY_BOT_ID)

class UnmockedTestCase(unittest.TestCase):

    def setUp(self):
        self.bot_help_test_params = [
            {
                KEY_INPUT: ["help", "about"],
                KEY_EXPECTED: {
                    'msg': "!!about - I will tell you a bit about myself",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT: ["help", "echo"],
                KEY_EXPECTED: {
                    'msg': "!!echo [message] - I will repeat whatever is after the echo command",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT: ["help", "funtranslate"],
                KEY_EXPECTED: {
                    'msg': "!!funtranslate [message] - I will translate whatever follows the command into a fun language",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT:  ["help", "joke"],
                KEY_EXPECTED: {
                    'msg': "!!joke - I will tell you great joke",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT: ["help"],
                KEY_EXPECTED: {
                    'msg': "!!help [command] - please specify the command you would like to know about (about, echo, funtranslate, or joke)",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT:  ["help", "some random other string"],
                KEY_EXPECTED: {
                    'msg': "!!help [command] - please specify the command you would like to know about (about, echo, funtranslate, or joke)",
                    'sender': KEY_BOT_ID
                    }
            }
        ]
        
        self.bot_about_test_params = [
            {
                KEY_INPUT: "",
                KEY_EXPECTED: {
                    'msg': "I am your friendly neighborhood DadBot, here to help. To see a list of my commands, type '!!help'",
                    'sender': KEY_BOT_ID
                    }
            }
        ]
        
        self.bot_echo_test_params = [
            {
                KEY_INPUT: ["echo"],
                KEY_EXPECTED: {
                    'msg': "",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT: ["echo", "this string gets repeated"],
                KEY_EXPECTED: {
                    'msg': "this string gets repeated",
                    'sender': KEY_BOT_ID
                    }
            }
        ]
        
        self.bot_error_test_params = [
            {
                KEY_INPUT: "",
                KEY_EXPECTED: {
                    'msg': "Sorry, '' is not a recognized command. To see a list of known commands, use '!!help'",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT: "NULL",
                KEY_EXPECTED: {
                    'msg': "Sorry, 'NULL' is not a recognized command. To see a list of known commands, use '!!help'",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT: "flibertygibbet",
                KEY_EXPECTED: {
                    'msg': "Sorry, 'flibertygibbet' is not a recognized command. To see a list of known commands, use '!!help'",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT: "Let's type a whole sentence here.",
                KEY_EXPECTED: {
                    'msg': "Sorry, 'Let's type a whole sentence here.' is not a recognized command. To see a list of known commands, use '!!help'",
                    'sender': KEY_BOT_ID
                    }
            }
        ]
        
        self.validURL_test_params = [
            {
                KEY_INPUT: "dsag",
                KEY_EXPECTED: False
            },
            {
                KEY_INPUT: "https://www.google.com",
                KEY_EXPECTED: True
            },
            {
                KEY_INPUT: "https://www.telegraph.co.uk/content/dam/Travel/2018/January/white-plane-sky.jpg?impolicy=logo-overlay",
                KEY_EXPECTED: True
            },
            {
                KEY_INPUT: "https://www.telegraph.co.uk/content/dam/Travel/2018/January/white-plane-sky.jpg",
                KEY_EXPECTED: True
            },
            {
                KEY_INPUT: "",
                KEY_EXPECTED: False
            }
        ]
        
        self.imageURL_test_params = [
            {
                KEY_INPUT: "dsag",
                KEY_EXPECTED: False
            },
            {
                KEY_INPUT: "https://www.google.com",
                KEY_EXPECTED: False
            },
            {
                KEY_INPUT: "https://www.telegraph.co.uk/content/dam/Travel/2018/January/white-plane-sky.jpg?impolicy=logo-overlay",
                KEY_EXPECTED: True
            },
            {
                KEY_INPUT: "https://www.telegraph.co.uk/content/dam/Travel/2018/January/white-plane-sky.jpg",
                KEY_EXPECTED: True
            },
            {
                KEY_INPUT: "",
                KEY_EXPECTED: False
            }
        ]
        
        self.adjustMessageHTML_test_params = [
            {
                KEY_INPUT: "Message with no images or URLs",
                KEY_EXPECTED: "Message with no images or URLs"
            },
            {
                KEY_INPUT: "https://www.google.com",
                KEY_EXPECTED: '<a href="https://www.google.com">https://www.google.com</a>'
            },
            {
                KEY_INPUT: "Message with words and a URL: https://www.google.com",
                KEY_EXPECTED: 'Message with words and a URL: <a href="https://www.google.com">https://www.google.com</a>'
            },
            {
                KEY_INPUT: "https://www.telegraph.co.uk/content/dam/Travel/2018/January/white-plane-sky.jpg",
                KEY_EXPECTED: '<img src="https://www.telegraph.co.uk/content/dam/Travel/2018/January/white-plane-sky.jpg" class="embeddedImage" />'
            },
            {
                KEY_INPUT: "Message with words and an image: https://www.telegraph.co.uk/content/dam/Travel/2018/January/white-plane-sky.jpg",
                KEY_EXPECTED: 'Message with words and an image: <img src="https://www.telegraph.co.uk/content/dam/Travel/2018/January/white-plane-sky.jpg" class="embeddedImage" />'
            },
            {
                KEY_INPUT: "Message with words, a URL, and an image: https://www.google.com https://www.telegraph.co.uk/content/dam/Travel/2018/January/white-plane-sky.jpg",
                KEY_EXPECTED: 'Message with words, a URL, and an image: <a href="https://www.google.com">https://www.google.com</a> <img src="https://www.telegraph.co.uk/content/dam/Travel/2018/January/white-plane-sky.jpg" class="embeddedImage" />'
            },
            {
                KEY_INPUT: "",
                KEY_EXPECTED: ''
            }
        ]


    def test_bot_help(self):
        for test in self.bot_help_test_params:
            response = testBot.help(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response['msg'], expected['msg'])
            self.assertEqual(response['sender'], expected['sender'])

    def test_bot_about(self):
        for test in self.bot_about_test_params:
            response = testBot.about()
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response['msg'], expected['msg'])
            self.assertEqual(response['sender'], expected['sender'])

    def test_bot_echo(self):
        for test in self.bot_echo_test_params:
            response = testBot.echo(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response['msg'], expected['msg'])
            self.assertEqual(response['sender'], expected['sender'])

    def test_bot_error(self):
        for test in self.bot_error_test_params:
            response = testBot.error(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response['msg'], expected['msg'])
            self.assertEqual(response['sender'], expected['sender'])
    
    def test_isValidURL(self):
        for test in self.validURL_test_params:
            response = testBot.isValidURL(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response, expected)
    
    def test_isImageURL(self):
        for test in self.imageURL_test_params:
            response = testBot.isImageURL(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response, expected)
    
    def test_adjustMessageHTML(self):
        for test in self.adjustMessageHTML_test_params:
            response = testBot.adjustMessageHTML(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response, expected)


if __name__ == '__main__':
    unittest.main()