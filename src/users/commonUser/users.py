import logger
from db.servers import Servers
from users.administrator.administrators import Administrator
from users.commonUser.commandUsers import RegisterUser
from users.userException import UserException
from users.baseUser import BaseUser
from webexteamssdk import WebexTeamsAPI
from webex_bot.webex_bot import WebexBot
from db.servers import Servers
from db.pr import Pr
from db.users import Users

log = logger.getLogger("users")

class User(BaseUser):

    def __init__(self, bot:WebexBot, api: WebexTeamsAPI, users_db:Users, pr_db:Pr, servers_db:Servers, token_config):
        super().__init__(api, users_db, servers_db, bot)
        self.pr_db = pr_db
        self.admin = Administrator(api, users_db, servers_db, bot, token_config) 
        self.add_command(RegisterUser(self))   
        
    def send_bot_started_message(self):    
        rooms = self.api.rooms.list()
        log.info(f'Bot started in rooms: {rooms}')
        for u in rooms:
            ids = u.title
            people = self.api.people.list(displayName=ids)            
            for p in people:
                account_name = p.emails[0].split('@')[0]
                if self.admin.is_admin(account_name):
                    log.info(f'Bot restart notify admin: {p.emails[0]}')
                    self.admin.add_admin(account_name)
                else:
                    log.info(f'Bot has user: {people}')
                    
            self.admin.notify_all("Bot restarted")
                    
    def register_user(self, user_name, name, email, admin):
        is_admin = False
        if admin is True:
            self.admin.add_admin(user_name)
            is_admin=True
        self.users_db.insert_user(user_name, email, name, admin)
        return(f"registered {user_name}. It is admin {is_admin}")        

    def clean_removed_pr(self, prs):
        pr_ids = [f"PR-{pr_dict['id']}" for pr_dict in prs]
        data = self.pr_db.get_all_prs_and_emails()    
        for pr in data:
            email = pr[0]
            pr_id = pr[1]
            if not pr_id in pr_ids:
                log.debug(f"PR {pr_id} is not present in the provided PR list. REMOVE IT !!!!")
                self.pr_db.remove_pr_details_by_email_and_pr(email, pr_id)
        log.debug(f"{data}")
               
    def inform_admin(self, msg):
        self.admin.notify_all(msg)
        
    def is_admin(self, user_name):
        return self.admin.is_admin(user_name)
    
    def get_admins(self):
        return self.admin.get_admins()
    
    def get_users(self):
        return self.users_db.get_all_users()
    
    def is_system_ready(self):
        '''
        Starts the server if there is at least one admin and the config of the same
        '''
        admins = self.get_admins()
        if not admins:
            return False
        data = self.servers_db.are_servers_configurated(admins[0])
        return data
        
        
    def get_jenkins_admin_data(self):
        """
        Retrieves Jenkins admin data from the database.
        This method fetches the Jenkins admin user, queries the database for the 
        admin's details, and returns the admin's username, Jenkins URL, project, 
        and token.
        Raises:
            UserException: If no Jenkins admin is found.
        Returns:
            tuple: A tuple containing the admin's username, Jenkins URL, project, 
            and token.
        """
        admins = self.admin.get_admins()
        if admins is None:
            raise UserException("No Jenkins admin found")
        data = self.servers_db.query_server_data_by_user_name_and_type(admins[0], Servers.JENKINS)
        try:
            url = data[0][Servers.URL_POS]
            project = data[0][Servers.PROJECT_POS]
            token = data[0][Servers.TOKEN_POS]
        except IndexError:
            raise UserException(f"No Jenkins server configured for {admins[0]}")
        
        return admins[0], url, project, token
        
    def get_server_data(self, server: str, admin: str): 
        if self.is_admin(admin):
           return self.admin.get_service_by_user(server, admin)
        else :
            raise UserException(f"{admin} is not and admin for {server}")
            
    def tokens_is_expiring(self, days):
        self.admin.tokens_is_expiring(days)
        
        