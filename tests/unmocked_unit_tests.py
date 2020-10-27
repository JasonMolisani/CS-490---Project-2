import unittest
import sys
sys.path.append('../')
import bot

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_BOT_ID = 42

testBot = bot.Bot(KEY_BOT_ID)

class UnmockedTestCase(unittest.TestCase):

    def setUp(self):
        self.success_test_bot_help = [
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
        
        self.failure_test_params = [
            {
                KEY_INPUT: "",
                KEY_EXPECTED: "a"
            }
        ]


    def test_success(self):
        for test in self.success_test_bot_help:
            response = testBot.help(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response['msg'], expected['msg'])
            self.assertEqual(response['sender'], expected['sender'])
            
    def test_failure(self):
        for test in self.failure_test_params:
            response = test[KEY_INPUT]
            expected = test[KEY_EXPECTED]
            
            self.assertNotEqual(response, expected)


if __name__ == '__main__':
    unittest.main()