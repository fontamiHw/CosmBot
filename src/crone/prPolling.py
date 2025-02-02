
import logger
from users.commonUser.users  import User
from cosm.sanity import Sanity
from crone.pollingBase import PollingBase


log = logger.getLogger("prPolling")

class PrPolling(PollingBase):
    def __init__(self, user:User, config):
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
                log.info("System just started and asking to Jenkins all jobs")
                self.total_pr=0
                self.task_ready = True

            self.main_loop()
                
    def main_loop(self):
        try:
            new_prs = self.sanity.collect_all_data_prs()
            log.debug(f"Total PRs found now: {new_prs['total-pr']}")
            if self.total_pr != new_prs['total-pr']:
                self.total_pr = new_prs['total-pr']
                log.debug(f"Different from previous Send to admin")
                self.handle_prs(new_prs)   
        except Exception as e:
            log.error(f"Error in PrPolling main loop: {e}")
            self.bitbucket.connect()
            self.total_pr = 0


    def stop(self):
        self.stop_event.set()
        self.thread.join()   

