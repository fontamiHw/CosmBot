import jenkins
import json
import logger
from users.userException import UserException
from servers.jenkins.jobEvent import process_job_event


log = logger.getLogger("EventProcessor")
class EventProcessor(object):


    def __init__(self, users, pr_db):
        self.users = users
        self.pr_db = pr_db
        self.start_jenkins_server()

    def compose_url(self, url, path):
        if path:
            return f"{url}/{path}"
        else:
            return url
        
    def start_jenkins_server(self):
        try :
            admin, url, path, token= self.users.get_jenkins_admin_data()
            self.server = jenkins.Jenkins(self.compose_url(url, path), username=admin, password=token)
            self.init=True
        except UserException as e:
            self.init=False    
            log.error(f"Error in jenkins server connection: {e}")   

        
    def event_received(self, event):
        if not self.init:
            self.start_jenkins_server()
            
        if event['type'] == 'all':
            return self.process_all_event()
        elif event['type'] == 'job':
            return self.process_job_event(event)
        else:
            raise ValueError("Unknown event type: {}".format(event['type']))
        
        
    def process_all_event(self):
        if not self.init:
            self.start_jenkins_server()
        ''' 
         process an array of :send_user_message
         {
          "_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob",
          "name": "PR-10671",
          "url": "https://engci-private-gpk.cisco.com/jenkins/svo/job/svo_multibranch/job/PR-10671/",
          "color": "red",
          "fullname": "PR-10671"
         }
        '''
        return_list = []
        try:
            jobs = self.server.get_jobs()
            log.debug(json.dumps(jobs, indent=2))
        
            for job in jobs:
                job_data = self.get_job_data(job['name'])
                new_dict = {"job": job['name'], "url": job['url'], "result": job_data}
                return_list.append(new_dict) 
        except Exception as e:
            log.warning(f"Cannot work with Jenkins server {e}")                    
        
        return return_list
    

    def process_job_event(self, event):
        job= event['job']
        emails = self.pr_db.query_emails_by_pr_and_triggers(job, event['status'])
        if emails:
            pr_data = self.get_job_data(job)
            process_job_event(emails, pr_data, self.users, event['status'])            
        return (f"notified {len(emails)} users for {job}")
        
        
    def get_job_data(self, job):
        if not self.init:
            self.start_jenkins_server()
        try:
            data = self.server.get_job_info(job)
            log.debug(f"Processing job= {job} : \n{json.dumps(data, indent=2)}")
            new_dict = {
                "lastStableBuild": data['lastStableBuild']['number'] if data['lastStableBuild'] else None,
                "lastStableBuildUrl": data['lastStableBuild']['url'] if data['lastStableBuild'] else None,
                "lastBuild": data['lastBuild']['number'] if data['lastBuild'] else None,
                "lastBuildUrl": data['lastBuild']['url'] if data['lastBuild'] else None,
                "lastCompletedBuild": data['lastCompletedBuild']['number'] if data['lastCompletedBuild'] else None,
                "lastCompletedBuildUrl": data['lastCompletedBuild']['url'] if data['lastCompletedBuild'] else None,
                "lastFailedBuild": data['lastFailedBuild']['number'] if data['lastFailedBuild'] else None,
                "lastFailedBuildUrl": data['lastFailedBuild']['url'] if data['lastFailedBuild'] else None,
                "url": data['url'],
                "name": data['name'],
                "color":data['color']
            }
        except Exception as e:
            log.error(f"fallito per {e}")
            return []

        log.debug(f"prd data {new_dict}")            
        return new_dict
    
    def get_job_data_from_git_pr(self, git):
        if not self.init:
            self.start_jenkins_server()

        ret = []
        jobs = self.server.get_jobs()
            
        for i in range(len(jobs)):
            pr = jobs[i]['name'].split("-")[1]
            for y in range(len(git['pr-list'])):
                if pr in str(git['pr-list'][y]['id']):
                    ret.append(jobs[i]) 
        return ret           
        