import logger
from users.baseUser import BaseUser
from db.servers import Servers

log = logger.getLogger("administrators")
class Administrator(BaseUser):

    def __init__(self, api, users_db, servers_db):
        super().__init__(api, users_db, servers_db)
        self.admins = list()
                
    def add_admin(self, admin):
        self.admins.append(admin)
                
    def remove_admin(self, admin):
        self.admins.remove(admin)
        
    def is_admin(self, user_name):
        return self.users_db.is_admin_by_userId(user_name)
                
    def notify(self, account_name, msg):
        if (self.is_admin(account_name)):
            email =self.users_db. get_email_by_userId(account_name)
            self.api.messages.create(toPersonEmail=email, markdown=msg)
                
    def notify_all(self, msg):
        for admin in self.admins:
            email =self.users_db.get_email_by_userId(admin)
            self.api.messages.create(toPersonEmail=email, markdown=msg)
                
    def get_admin(self):
        if self.admins:
            return self.admins[0]
        else:
            return None
        
    def tokens_is_expiring(self, days):
        log.debug("Checking tokens expiration")
        tokens = self.servers_db.get_all_token_closer_expiration(days)
        
        for admin in self.admins:
            log.debug(f"Checking tokens expiration for {admin}")
            admin_tokens = [token for token in tokens if token['user_name'] == admin]
            
            for token in admin_tokens:
                log.debug(f"Token {token['type']} is expiring in {token['remaining_days']} days")
                email = self.users_db.get_email_by_userId(admin)
                title = f"# Your token is expiring in {token['remaining_days']} days\n"
                message = f"It is urgent to update your token. Please do it as soon as possible. \n\n"
                command= f"When ready run the command `server config`\n and insert only the **{token['type']} server** , **username** and new **token**"
                self.send_user_message(email, f"{title} {message} {command}")
        