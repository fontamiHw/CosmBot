

class PollingBase(object):
    def __init__(self, interval, callback, unit_of_measure_interval='seconds'):
        self.interval = interval
        self.callback = callback
        self.unit_of_measure_interval = unit_of_measure_interval
        
    def get_polling_interval(self):
        return self.interval
    
    def get_task(self):
        return self.callback
    
    def get_unit_of_measure_interval(self):
        return self.unit_of_measure_interval