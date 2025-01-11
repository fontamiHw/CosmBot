import logger
from db.servers import Servers
from users.administrator.administrators import Administrator
from users.commonUser.commandUsers import RegisterUser
from webexteamssdk.api import people
from cosmException import CosmException
from users.userException import UserException
from users.baseUser import BaseUser

log = logger.getLogger("users")

class User(BaseUser):

    def __init__(self, bot, api, users_db, pr_db, servers_db, token_config):
        super().__init__(api, users_db, servers_db, bot)
        self.pr_db = pr_db
        self.admin = Administrator(api, users_db, servers_db, bot, token_config) 
        self.add_command(RegisterUser(self))       
        
        for u in api.rooms.list():
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
        admin = self.get_admins()[0]
        if admin:
            data = self.servers_db.are_servers_configurated(admin)
            return data
        return False
        
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
        admin = self.admin.get_admins()[0]
        if admin is None:
            raise UserException("No Jenkins admin found")
        data = self.servers_db.query_server_data_by_user_name_and_type(admin, Servers.JENKINS)
        try:
            url = data[0][Servers.URL_POS]
            project = data[0][Servers.PROJECT_POS]
            token = data[0][Servers.TOKEN_POS]
        except IndexError:
            raise UserException(f"No Jenkins server configured for {admin}")
        
        return admin, url, project, token
        
    def register_in_server(self, server_name, url, project, user, token, token_expiration):    
        msg=""
        if self.servers_db.user_in_server(user, server_name) :
            log.info(f"{user} already in {server_name}, update with new values")
            if token_expiration and not token:
                raise CosmException(f"Cannot change expiration days without a new token")
            self.servers_db.update_server_user(user, url, project, token, server_name, token_expiration)
            msg = f"{user} updated in {server_name} with url {url} and project {project}"
        else:     
            log.info(f"{user} not in {server_name}, add it")       
            if not url or not server_name or not token:
                raise CosmException(f"{user} has no server {server_name} configured. \n All the elements shall be compiled.")
            self.servers_db.insert_server_user(user, url, project, token, server_name, token_expiration) 
            msg = f"{user} added in {server_name} with url {url} and project {project}"
            
        log.info(msg)
        
    def get_server_data(self, server, admin): 
        if self.is_admin(admin):
           return self.admin.get_service_by_user(server, admin)
            
    def tokens_is_expiring(self, days):
        self.admin.tokens_is_expiring(days)
        
        