import flask_socketio
import requests

MAX_MESSAGE_LENGTH = 120

class Bot:
    def __init__(self, DB_Id=0):
        self.DB_Id = DB_Id
    
    def parseCommand(self, message):
        commandArgs = message.split(maxsplit=1)
        if len(commandArgs) < 1:
            return self.error("NULL")
        elif commandArgs[0]=="help":
            return self.help(commandArgs)
        elif commandArgs[0] == "about":
            return self.about()
        elif commandArgs[0] == "joke":
            return self.joke()
        elif commandArgs[0] == "echo":
            return self.echo(commandArgs)
        elif commandArgs[0] == "funtranslate":
            return self.funtranslate(commandArgs)
        else:
            return self.error(commandArgs[0])
    
    def help(self, cmdArgs):
        if len(cmdArgs) >= 2:
            if cmdArgs[1] == 'about':
                hlpMsg = "!!about - I will tell you a bit about myself"
            elif cmdArgs[1] == 'echo':
                hlpMsg = "!!echo [message] - I will repeat whatever is after the echo command"
            elif cmdArgs[1] == 'funtranslate':
                hlpMsg = "!!funtranslate [message] - I will translate whatever follows the command into a fun language"
            elif cmdArgs[1] == 'joke':
                hlpMsg = "!!joke - I will tell you great joke"
            else:
                # Return the default message (defined below)
                return self.help([cmdArgs[0]])
        else:
            hlpMsg = "!!help [command] - please specify the command you would like to know about (about, echo, funtranslate, or joke)"
        return {'msg': hlpMsg, 'sender': self.DB_Id}
    
    def about(self):
        abtMsg = "I am your friendly neighborhood DadBot, here to help. To see a list of my commands, type '!!help'"
        return {'msg': abtMsg, 'sender': self.DB_Id}
    
    def echo(self, cmdArgs):
        echoMsg = ""
        if len(cmdArgs) >= 2:
            echoMsg += cmdArgs[1]
        return {'msg': echoMsg, 'sender': self.DB_Id}
    
    def funtranslate(self, cmdArgs):
        trnsMsg = ""
        if len(cmdArgs) >= 2:
            trnsMsg += cmdArgs[1]
        # TODO implement use of funtranslate API
        parameters = {"text": trnsMsg}
        response = requests.get("https://api.funtranslations.com/translate/pirate.json", params=parameters)
        if response.status_code == 200:
            trnsMsg = response.json()["contents"]["translated"]
        if len(trnsMsg) > MAX_MESSAGE_LENGTH:
            trnsMsg = trnsMsg[:MAX_MESSAGE_LENGTH]
        return {'msg': trnsMsg, 'sender': self.DB_Id}
    
    def joke(self):
        # Uses the icanhazdadjoke API to get a dad joke
        header = {"user-agent": "Student Chat App (author: https://github.com/JasonMolisani)", "Accept": "application/json"}
        foundJoke = False
        for i in range(5):
            response = requests.get("https://icanhazdadjoke.com/", headers=header)
            if response.status_code == 200:
                if len(response.json()["joke"]) < MAX_MESSAGE_LENGTH:
                    foundJoke = True
                    break
                else:
                    print(response.json())
        if foundJoke:
            jkMsg = response.json()['joke']
        else:
            jkMsg = "Sorry, I can't seem to think of a good joke right now"
        return {'msg': jkMsg, 'sender': self.DB_Id}
    
    def error(self, badCommand):
        errMsg = "Sorry, '{}' is not a recognized command.".format(badCommand)
        errMsg += " To see a list of known commands, use '!!help'"
        return {'msg': errMsg, 'sender': self.DB_Id}
