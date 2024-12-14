import os
import time
import logger
import threading
import yaml

from cosm.sanity import Sanity
from db.servers import Servers
from db.pr import Pr
from db.users import Users
from servers.git.bitbucket import Git
from servers.web.webserver  import  WebServer
from servers.jenkins.jenkins import EventProcessor
from servers.prPolling import PrPolling
from users.users import User
from webex_bot.webex_bot import WebexBot
from webexteamssdk import WebexTeamsAPI



log = logger.getLogger()

def start_servers(config, bot, api, git, jenkins_event, sanity):    
    task = PrPolling(user, config['pr'], sanity)
    task.start()
    
    web = WebServer(jenkins_event)
    web.start()

def test(data):
    log.info(f"from server arrived {data}")
    
def create_db(config):    
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
    
    
def init_bot(config):
    api = WebexTeamsAPI(access_token=config['webexBot']['token'])   
    
    # (Optional) Proxy configuration
    # Supports https or wss proxy, wss prioritized.
    proxies = {
        'https': 'http://proxy.esl.cisco.com:80',
        'wss': 'socks5://proxy.esl.cisco.com:1080'
    }
    
    # Create a Bot Object
    bot = WebexBot(teams_bot_token=config['webexBot']['token'],
                   approved_domains=['cisco.com'],
                   bot_name=config['webexBot']['name'],
                   include_demo_commands=True,
                   proxies=proxies)
    return bot, api



def run():
    while not user.is_system_ready():
        time.sleep(20)

    git = Git(config['pr']['gitServer'], user, servers_db.query_server_data_by_user_name_and_type(user.get_admin(), Servers.GIT) )
    jenkins_event = EventProcessor(user, prDb)
    sanity = Sanity(bot, api, prDb, git, jenkins_event, user)
    start_servers(config, bot, api, git, jenkins_event, sanity)    
   


def stop(self):
    stop_event.set()
    thread.join()
    
      
# Load configuration from YAML file
with open('../resources/config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    
usersDb, prDb, servers_db= create_db(config['database'])
bot, api = init_bot(config)
user = User(bot, api, usersDb, prDb, servers_db)

thread = threading.Thread(target=run)
stop_event = threading.Event()
thread.start()
log.info("Bot started")
# Call `run` for the bot to wait for incoming messages.
bot.run()
    