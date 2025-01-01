from cosm.command.prCommand import PrRegister, PrStatus
import logger


log = logger.getLogger("sanity")
class Sanity(object):
    '''
    classdocs
    '''

    def __init__(self, bot, api, db, git, jenkins_event, user):
        self.api = api
        self.bot = bot
        self.pr_db = db
        self.git = git
        self.jenkins_event =  jenkins_event
        self.add_commands()
        self.git.connect()
        self.user = user
        
    def add_commands(self):
        #add any user command
        self.bot.add_command(PrRegister(self.pr_db))
        self.bot.add_command(PrStatus(self))
        

    def collect_all_data_prs(self):
        total_pr, open_pull_requests = self.git.get_open_pr()
        jenkins_data = self.jenkins_event.process_all_event()
        self.new_dict = {"total-pr": total_pr, "open-pr": open_pull_requests, "jenkins": jenkins_data}
        return self.new_dict

    def get_total_pr_message(self ):
        total_pr = self.new_dict['total-pr']
        open_pull_requests = self.new_dict['open-pr']
        jenkins_data = self.new_dict['jenkins']
        mdList = ''
        # Create a set of ids from the first list
        # pr_set = {f"PR-{str(item['id'])}" for item in open_pull_requests}
        for jenkins_pr in jenkins_data:
            git_data = self.git_from_jenkins(jenkins_pr['job'], open_pull_requests)
            if git_data:
                last_completed_build= 0
                last_failed_build= 0
                if jenkins_pr['result']['lastCompletedBuild']:
                    last_completed_build = jenkins_pr['result']['lastCompletedBuild']
                if jenkins_pr['result']['lastFailedBuild']:
                    last_failed_build = jenkins_pr['result']['lastFailedBuild']
                  
                build_link = f"[{last_completed_build}]({jenkins_pr['url']}) / [{last_failed_build}]({jenkins_pr['url']})"
                if (last_failed_build >= last_completed_build):
                    build_link = f"[{last_completed_build}]({jenkins_pr['url']}) / [{last_failed_build} FAILED]({jenkins_pr['url']})"
                
                pr_link = f"[{git_data['id']}]({git_data['url']})" 
                mdList += f" {pr_link} {git_data['title']} {build_link} \n" 
        return(f'# There are currently {total_pr} PRs:\n{mdList}')


    #-- private method    

    def git_from_jenkins(self, job, git_list):
        for git in git_list:
            if str(git['id']) in job:
                return {"id":git['id'], "url":git['href'], "title":git['title']}
        return None  