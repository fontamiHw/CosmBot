import logger, shutil
from users.commonUser.users import User
from servers.socket.commands.baseClass.userBaseCommands import UserBaseCommands
from users.userException import UserException

class DatabaseCommands(UserBaseCommands):

    def __init__(self, users:User, config_db):
        super().__init__(users)
        self.config_db = config_db
        self.log = logger.getLogger("DatabaseCommands")  
        
    def process_command(self, command, data):
        try:
            src=self.config_db['directory']
            dst = "/app/host/files"      
            file = self.config_db[data['db']]['dbname']         
            if file :
                try:
                    self.log.info(f"copying {src}/{file} to {dst}")
                    if shutil.copy(f"{src}/{file}", dst):
                        return {"file-copied": file}
                    else :
                        raise UserException(f"Error copying {file} from {src} to {dst}")
                except Exception as e:
                    raise UserException(f"Error copying {file} from {src} to {dst} due to {e}")
        except Exception as e:
            raise UserException(f"{data['db']} is an unknown deatabase")
    