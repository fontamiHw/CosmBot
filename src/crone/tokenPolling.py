import logger
from db.users import Users
from crone.pollingBase import PollingBase


log = logger.getLogger("TokenPolling")

class TokenPolling(PollingBase):
    def __init__(self, user: Users, expiration_days: int):
        super().__init__(expiration_days, self.run, unit_of_measure_interval='days')
        self.user = user
        self.expiration_days = expiration_days
        
    def run(self): 
        try:  
            log.debug("Check if some token is expiring")  
            self.user.tokens_is_expiring(self.expiration_days)   
        except Exception as e:
            log.error(f"Error in TokenPolling: {e}")