import unittest
import sys
sys.path.append('../') # Allow for imports to work when run from within test folder
sys.path.append('./')  # Allow for imports to work when run from within project2 folder
import bot
import unittest.mock as mock
import json
import app
from app import db
from io import StringIO

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_BOT_ID = 42
KEY_CHANNEL = 'channel'
KEY_DATA = 'data'
KEY_NUM_USERS = 'numUsers'
KEY_USER_LIST = 'loggedInUsers'
KEY_REQUEST_SID = 'sid'
KEY_CHAT_HISTORY = 'chtHist'

testBot = bot.Bot(KEY_BOT_ID)

class Mock_Request:
    def __init__(self, json_str=''):
        self.json_str = json_str
        self.status_code = 200
    
    def json(self):
        return json.loads(self.json_str)
        
class Mock_DB:
    def __init__(self, dataList):
        self.data = dataList
    
    def all(self):
        return self.data
        
class Mock_Senders_DB:
    def __init__(self, dataList):
        self.data = dataList
    
    def all(self):
        return self.data
    
    def filter_by(self, id="pic0.jpg"):
        matching = []
        for sender in self.data:
            if sender.picUrl == id:
                matching.append(sender)
        return Mock_DB(matching)

class Mock_DB_Sender:
    def __init__(self, senderPic, senderEmail):
        self.picUrl = senderPic
        self.email = senderEmail

class Mock_DB_Message:
    def __init__(self, senderPic='', message='', clss='user', senderEmail=''):
        self.sender = Mock_DB_Sender(senderPic, senderEmail)
        self.message = message
        self.senderClass = clss
    
    def __repr__(self):
        return json.dumps({'sender': self.sender.picUrl, 'message': self.message, 'class': self.senderClass})

class MockedTestCase(unittest.TestCase):
    def setUp(self):
        self.bot_parseCommand_test_params = [
            {
                KEY_INPUT: "joke",
                KEY_EXPECTED: {
                    'msg': "Insert dad joke here",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT: "funtranslate",
                KEY_EXPECTED: {
                    'msg': "Insert translated pirate text here",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT: "help about",
                KEY_EXPECTED: {
                    'msg': "!!about - I will tell you a bit about myself",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT: "echo bunch of words",
                KEY_EXPECTED: {
                    'msg': "bunch of words",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT: "about other nonsense",
                KEY_EXPECTED: {
                    'msg': "I am your friendly neighborhood DadBot, here to help. To see a list of my commands, type '!!help'",
                    'sender': KEY_BOT_ID
                    }
            },
            {
                KEY_INPUT: "",
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
            }
        ]
        
        self.app_on_connect_test_params = [
            {
                KEY_INPUT: {
                    KEY_NUM_USERS: 0
                },
                KEY_EXPECTED: {
                    KEY_CHANNEL: 'someone connected',
                    KEY_DATA: {
                        KEY_NUM_USERS: 0
                    }
                }
            }
        ]
        
        self.app_on_disconnect_test_params = [
            {
                KEY_INPUT: {
                    KEY_NUM_USERS: 10,
                    KEY_USER_LIST: {0, 1, 2, 3},
                    KEY_REQUEST_SID: 1
                },
                KEY_EXPECTED: {
                    KEY_CHANNEL: 'someone disconnected',
                    KEY_DATA: {
                        KEY_NUM_USERS: 9
                    }
                }
            },
            {
                KEY_INPUT: {
                    KEY_NUM_USERS: 10,
                    KEY_USER_LIST: {0, 1, 2, 3},
                    KEY_REQUEST_SID: 4
                },
                KEY_EXPECTED: {
                    KEY_CHANNEL: 'someone disconnected',
                    KEY_DATA: {
                        KEY_NUM_USERS: 10
                    }
                }
            }
        ]
        
        self.app_emit_chat_history_test_params = [
            {
                KEY_INPUT: {
                    KEY_CHAT_HISTORY: [
                            Mock_DB_Message("pic1.jpg", "!!help", "user", "fake1@bogus.com"),
                            Mock_DB_Message("picBot.jpg", "!!help [command] - please specify the command you would like to know about (about, echo, funtranslate, or joke)", "bot", "bot@bogus.com")
                        ],
                    KEY_USER_LIST: {1},
                    KEY_CHANNEL: 'test broadcast'
                },
                KEY_EXPECTED: {
                    KEY_CHANNEL: 'test broadcast',
                    KEY_DATA: {
                        'chatHistory': [
                            {
                                'senderPic': "pic1.jpg",
                                'message': '!!help',
                                'class': 'user'
                            },
                            {
                                'senderPic': "picBot.jpg",
                                'message': '!!help [command] - please specify the command you would like to know about (about, echo, funtranslate, or joke)',
                                'class': 'bot'
                            }
                        ]
                    }
                }
            }
        ]
        
        self.app_on_new_message_test_params = [
            {
                KEY_INPUT: {
                    KEY_DATA: {
                        'sender': "pic1.jpg",
                        'msg': "Random message"
                    },
                    KEY_USER_LIST: [
                        Mock_DB_Sender('pic1.jpg', '')
                    ]
                },
                KEY_EXPECTED: {
                    'sender': 'pic1.jpg',
                    'message': 'Random message', 
                    'class': 'user'
                }
            }
        ]

    @staticmethod
    def mock_request_response(url, params={}, headers={}):
        if (url == "https://api.funtranslations.com/translate/pirate.json"):
            resp =  {
                        'contents': {
                            'translated': "Insert translated pirate text here"
                        }
                    }
        elif (url == "https://icanhazdadjoke.com/"):
            resp =  {
                        'joke': "Insert dad joke here"
                    }
        resp_obj = Mock_Request(json.dumps(resp, indent = 4))
        return resp_obj
    
    @staticmethod
    def mock_emit(channel, data, room=0):
        resp = {
            KEY_CHANNEL: channel,
            KEY_DATA: data
        }
        
        raise NameError(json.dumps(resp))
        
    @staticmethod
    def mock_null(anySingleArg=None):
        # Do Nothing
        return
    
    def mock_null_class(self, anySingleArg=None):
        return
        
    @staticmethod
    def mock_add(destinationDB, DBentry):
        
        raise NameError(str(DBentry))

    def test_bot_parseCommands(self):
        for test in self.bot_parseCommand_test_params:
            with mock.patch('requests.get', self.mock_request_response):
                response = testBot.parseCommand(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response['msg'], expected['msg'])
            self.assertEqual(response['sender'], expected['sender'])
    
    def test_app_on_connect(self):
        for test in self.app_on_connect_test_params:
            global initialNumUsers
            initialNumUsers = test[KEY_INPUT][KEY_NUM_USERS]
            with mock.patch('app.socketio.emit', self.mock_emit):
                try:
                    app.on_connect()
                    self.assertEqual("no mocked emit sent", "")
                except NameError as response_str:
                    response = json.loads(str(response_str))
                    expected = test[KEY_EXPECTED]
                    
                    self.assertEqual(response[KEY_CHANNEL], expected[KEY_CHANNEL])
                    self.assertEqual(response[KEY_DATA], expected[KEY_DATA])
    
    # def test_app_on_disconnect(self):
    #     for test in self.app_on_disconnect_test_params:
    #         global initialNumUsers
    #         initialNumUsers = test[KEY_INPUT][KEY_NUM_USERS]
    #         global loggedInUsers
    #         loggedInUsers = test[KEY_INPUT][KEY_USER_LIST]
    #         with mock.patch('app.socketio.emit', self.mock_emit):
    #             try:
    #                 with mock.patch('flask.request.sid', test[KEY_INPUT][KEY_REQUEST_SID]):
    #                     on_disconnect()
    #                 self.assertEqual("no mocked emit sent", "")
    #             except NameError as response_str:
    #                 response = json.loads(str(response_str))
    #                 expected = test[KEY_EXPECTED]
                    
    #                 self.assertEqual(response[KEY_CHANNEL], expected[KEY_CHANNEL])
    #                 self.assertEqual(response[KEY_DATA], expected[KEY_DATA])
    @mock.patch('sqlalchemy.orm.session.Session.query', Mock_DB)
    def test_emit_chat_history(self):
        for test in self.app_emit_chat_history_test_params:
            fakeDB = test[KEY_INPUT][KEY_CHAT_HISTORY]
            with mock.patch('app.socketio.emit', self.mock_emit):
                with mock.patch('app.loggedInUsers', test[KEY_INPUT][KEY_USER_LIST]):
                    try:
                        with mock.patch('models.chatHistory', fakeDB):
                            app.emit_chat_history(test[KEY_INPUT][KEY_CHANNEL])
                        self.assertEqual("no mocked emit sent", "")
                    except NameError as response_str:
                        response = json.loads(str(response_str))
                        expected = test[KEY_EXPECTED]
                        
                        self.assertEqual(response[KEY_CHANNEL], expected[KEY_CHANNEL])
                        self.assertEqual(response[KEY_DATA], expected[KEY_DATA])

    @mock.patch('models.chatHistory', Mock_DB_Message)
    @mock.patch('sqlalchemy.orm.session.Session.commit', mock_null)
    @mock.patch('app.emit_chat_history', mock_null_class)
    def test_on_new_message(self):
        for test in self.app_on_new_message_test_params:
            with mock.patch('models.registeredUsers.query', Mock_Senders_DB(test[KEY_INPUT][KEY_USER_LIST])):
                with mock.patch('sqlalchemy.orm.session.Session.add', self.mock_add):
                    try:
                        app.on_new_message(test[KEY_INPUT][KEY_DATA])
                        assertEqual("Added to DB", "")
                    except NameError as resp_str:
                        response = json.loads(str(resp_str))
                        
                        self.assertEqual(response, test[KEY_EXPECTED])

if __name__ == '__main__':
    unittest.main()