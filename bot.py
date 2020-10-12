import flask_socketio

class Bot:
    def __init__(self, name="DadBot"):
        self.name = name
    
    def parseCommand(self, message):
        commandArgs = message.split(maxsplit=1)
        if len(commandArgs) < 1:
            return self.error("NULL")
        elif commandArgs[0]=="help":
            return self.help(commandArgs)
        elif commandArgs[0] == "about":
            return self.about()
        elif commandArgs[0] == "echo":
            return self.echo(commandArgs)
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
            else:
                # Return the default message (defined below)
                return self.help([cmdArgs[0]])
        else:
            hlpMsg = "!!help [command] - please specify the command you would like to know about (about, echo, funtranslate, or TBD)"
        return {'msg': hlpMsg, 'sender': self.name}
    
    def about(self):
        abtMsg = "I am your friendly neighborhood DadBot, here to help. To see a list of my commands, type '!!help'"
        return {'msg': abtMsg, 'sender': self.name}
    
    def echo(self, cmdArgs):
        echoMsg = ""
        if len(cmdArgs) >= 2:
            echoMsg += cmdArgs[1]
        return {'msg': echoMsg, 'sender': self.name}
    
    def error(self, badCommand):
        errMsg = "Sorry, '{}' is not a recognized command.".format(badCommand)
        errMsg += " To see a list of known commands, use '!!help'"
        return {'msg': errMsg, 'sender': self.name}
