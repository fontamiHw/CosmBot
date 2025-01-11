import logger
from users.baseUser import BaseUser
from users.administrator.commandAdmin import RegisterServer
import json

log = logger.getLogger("administrators")
class Administrator(BaseUser):

    def __init__(self, api, users_db, servers_db, bot, token_config):
        super().__init__(api, users_db, servers_db, bot)
        self.admins = list()        
        self.add_command(RegisterServer(self))
        self.refreshLinks = token_config['refreshLinks']
                
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
                
    def get_admins(self):
        if self.admins:
            return self.admins
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
                user_name = f"{token['user_name']}"
                
              
                link = next((item['tokenLink'] for item in self.refreshLinks if item['name'] == token['type']), None)
                link = link.replace("{user_name}", user_name)
                title = f"# Your {token['type']} token is expiring in {token['remaining_days']} days\n"
                message = f"It is urgent to [update your token]({link}). Please do it as soon as possible. \n\n"
                command= f"When ready run the command `server config`\n and insert only the **{token['type']} server** , **username** and new **token**"
                self.send_user_message(email, f"{title} {message} {command}")
        
    # Function to get all services for a specific user
    def get_service_by_user(self, server, user_name):       
        services = self.servers_db.get_service_by_user_and_type(user_name, server.lower())
        services_list = []
        for service in services:
            services_list.append({
                    'url': service[1],
                    'user_name': service[2],
                    'project': service[3],
                    'token': service[4],
                    'expiration-date': service[5]
            })
        return json.dumps(services_list)