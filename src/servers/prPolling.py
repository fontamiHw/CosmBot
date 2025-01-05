import threading
import time
import logger


log = logger.getLogger("prPolling")

class PrPolling:
    def __init__(self, user, config, sanity):
        self.interval = config['polling']  # Interval in seconds (600 seconds = 10 minutes)
        self.thread = threading.Thread(target=self.run)
        self.stop_event = threading.Event()
        self.sanity = sanity
        self.user = user

    def start(self):
        self.thread.start()
        
    def handle_prs(self, data):
        self.user.clean_removed_pr(data['open-pr'])
        self.user.inform_admin(self.sanity.get_total_pr_message()) 
        
    def run(self): 
        data = self.sanity.collect_all_data_prs()  
        total_pr = data['total-pr']
        self.handle_prs(data)
        self.user.inform_admin(self.sanity.get_total_pr_message())     
        while not self.stop_event.is_set():
            try:
                time.sleep(self.interval)
                new_prs = self.sanity.collect_all_data_prs()
                if total_pr != new_prs['total-pr']:
                    total_pr = new_prs['total-pr']
                    self.handle_prs(new_prs)                      
            except Exception:
                self.bitbucket.connect()


    def stop(self):
        self.stop_event.set()
        self.thread.join()   

class TokenPolling:
    def __init__(self, user, expiration_days):
        self.thread = threading.Thread(target=self.run)
        self.stop_event = threading.Event()
        self.user = user
        self.expiration_days = expiration_days

    def start(self):
        self.thread.start()
        
    def run(self): 
        log.info("TokenPolling started")  
        while True:
            try:  
                log.debug("Check if some token is expiring")  
                self.user.tokens_is_expiring(self.expiration_days)   
                time.sleep(86400)  # 1 day in seconds      
            except Exception as e:
                log.error(f"Error in TokenPolling: {e}")