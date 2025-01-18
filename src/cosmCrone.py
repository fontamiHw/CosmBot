
from db.users import Users
from cosm.sanity import Sanity
from crone.pollingBase import PollingBase
from crone.prPolling import PrPolling
from crone.tokenPolling import TokenPolling
import schedule, time
import threading, logger

log = logger.getLogger("CosmCrone")

class CosmCrone:
    def __init__(self):
        self.tasks = []
        self.thread = threading.Thread(target=self.execute)
        self.stop_event = threading.Event()    
        
    def run(self):
        self.thread.start()
        
    def execute(self):
        while True:                        
            time.sleep(1)
            schedule.run_pending()
        
    def start_task(self, task: PollingBase):
        self.tasks.append(task)
        interval = task.get_polling_interval()
        task_cb = task.get_task()
        if task.get_unit_of_measure_interval() == 'seconds':
            schedule.every(interval).seconds.do(task_cb)

        elif task.unit_of_measure_interval == 'days':
            schedule.every(interval).days.do(task_cb)
        
        jobs = schedule.get_jobs()
        log.info(f"configured crone task: {jobs}")
