
import logger
from db.users import Users
from cosm.sanity import Sanity
from crone.pollingBase import PollingBase


log = logger.getLogger("prPolling")

class PrPolling(PollingBase):
    def __init__(self, user: Users, config):
        super().__init__(config['polling'], self.run)# Interval in seconds (600 seconds = 10 minutes)
        self.sanity = None
        self.user = user
        self.task_ready = False
        self.total_pr = 0

    def add_sanity(self, sanity:Sanity):
        self.sanity = sanity
        
    def handle_prs(self, data):
        self.user.clean_removed_pr(data['open-pr'])
        self.user.inform_admin(self.sanity.get_total_pr_message()) 
        
    def run(self): 
        if not self.sanity:
            log.error("Sanity is not set")
            return
        else :
            if not self.task_ready:
                self.task_ready = True
                data = self.sanity.collect_all_data_prs()  
                self.total_pr = data['total-pr']
                self.handle_prs(data)
                self.main_loop()
            else:
                self.main_loop()
                
    def main_loop(self):
        try:
            new_prs = self.sanity.collect_all_data_prs()
            if self.total_pr != new_prs['total-pr']:
                self.total_pr = new_prs['total-pr']
                self.handle_prs(new_prs)   
        except Exception:
            self.bitbucket.connect()
            self.total_pr = 0


    def stop(self):
        self.stop_event.set()
        self.thread.join()   

