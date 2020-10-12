import flask_socketio

class Bot:
    def __init__(self, name="DragonBot"):
        self.name = name
    
    def parseCommand(self, message):
        commandArgs = message.split(maxsplit=1)
        if len(commandArgs) < 1:
            return self.error("NULL")
        elif commandArgs[0]=="help":
            return self.help()
        elif commandArgs[0] == "about":
            return self.about()
        else:
            return self.error(commandArgs[0])
    
    def help(self):
        hlpMsg = "Insert HELP message here" # TODO
        return {'msg': hlpMsg, 'sender': self.name}
    
    def about(self):
        abtMsg = "Insert ABOUT message here" # TODO
        return {'msg': abtMsg, 'sender': self.name}
    
    def error(self, badCommand):
        errMsg = "Sorry, '{}' is not a recognized command".format(badCommand)
        return {'msg': errMsg, 'sender': self.name}
