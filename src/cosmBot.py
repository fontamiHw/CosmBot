import os
import time
import threading

from cosm.sanity import Sanity
from db.servers import Servers
from db.pr import Pr
from db.users import Users
from servers.git.bitbucket import Git
from servers.jenkins.jenkins import EventProcessor
from crone.prPolling import PrPolling
from crone.tokenPolling import TokenPolling
from users.commonUser.users import User
from webex_bot.webex_bot import WebexBot
from webexteamssdk import WebexTeamsAPI
from servers.socket.clientSocket import ClientSocket
from cosmCrone import CosmCrone

import logger 


class CosmBot (object):
    def __init__(self, config):
        self.config = config
        self.log = logger.getLogger("CosmBot")  
        self.log.info("CosmBot - created")
        
        
    def bot_start(self):
        self.log.info("CosmBot - start")
    
        db_path = self.config['database']['directory']
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            self.log.info(f"Directory created: {db_path}")
        usersDb, self.prDb, self.servers_db= self.create_db(self.config['database'])
        self.bot, self.api, self.proxie = self.init_bot()
        self.user = User(self.bot, self.api, usersDb, self.prDb, self.servers_db, self.config['servers']['token'])

        self.thread = threading.Thread(target=self.run)
        self.stop_event = threading.Event()
        self.thread.start()
        self.log.info("Bot started")
        # Call `run` for the bot to wait for incoming messages.
        self.bot.run()
    
    def main_stop(self):
        self.main_stop_event.set()
        self.main_thread.join()        
    
    def run(self):
        if self.proxie:
            self.log.info("wait a wail because proxy")
            time.sleep(10)
            
        self.log.info("delayed initialization started")

        
        jenkins_event = EventProcessor(self.user, self.prDb)
        self.client = ClientSocket(self.config['container_communication'], self.config['database'], jenkins_event, self.user)
        
        self.user.send_bot_started_message()
        while not self.user.is_system_ready():
            time.sleep(20)
            
        pr_crone = self.start_crone_services()
                
        # do not need all admins just take the first
        self.git = Git(self.config['servers']['gitServer'], 
                       self.servers_db.query_server_data_by_user_name_and_type(self.user.get_admins()[0], Servers.GIT) )        
        self.log.info("  Git intialized")
        
        
        sanity = Sanity(self.bot, self.api, self.prDb, 
                        self.git, jenkins_event, self.user)  
        pr_crone.add_sanity(sanity)
        self.log.info("  Sanity intialized and added to Pr Crone")
        
        
        self.log.info("delayed initialization completed !!!")
        
    def start_crone_services(self):
        self.log.info("  Starting crone services")
        self.crone = CosmCrone()
        self.crone.run()
                
        token_polling = TokenPolling(self.user, self.config['servers']['token']['token_expiration_days'])
        self.crone.start_task(token_polling)
        self.log.info("    Token Crone service started")
        
        pr_crone = PrPolling(self.user, self.config['pr'])
        self.crone.start_task(pr_crone)
        self.log.info("    Pr Crone service started")
        return pr_crone
        
    def create_db(self, config):
        # Get the directory from the configuration
        db_directory = config['directory']
        db_name = config['users']['dbname']
        db_path = os.path.join(db_directory, db_name)
        user_db = Users(db_path)
    
        db_name = config['servers']['dbname']
        db_path = os.path.join(db_directory, db_name)
        servers_db = Servers(db_path)

        db_name = config['pr']['dbname']
        db_path = os.path.join(db_directory, db_name)
        pr = Pr(db_path)
    
        return user_db, pr, servers_db
    
    
    def init_bot(self):
        api = WebexTeamsAPI(access_token=self.config['webexBot']['token'])   
    
        proxies=None
        if self.config['webexBot']['proxy']['required']:
            # (Optional) Proxy configuration
            # Supports https or wss proxy, wss prioritized.
            proxies = self.config['webexBot']['proxy']['proxies']
            self.log.info(f" Proxies:{proxies}")
    
        # Create a Bot Object
        self.log.info(f"Bot name: {self.config['webexBot']['name']}")
        bot = WebexBot(teams_bot_token=self.config['webexBot']['token'],
                   approved_domains=['cisco.com'],
                   bot_name=self.config['webexBot']['name'],
                   include_demo_commands=True,
                   proxies=proxies)
        self.log.info(f"Bot created")
        return bot, api, proxies
    
    def stop(self):
        self.stop_event.set()
        self.thread.join()
