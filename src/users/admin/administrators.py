import logger


log = logger.getLogger()
class Administrator(object):

    def __init__(self, api, users_db):
        self.users_db = users_db
        self.api = api
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
        