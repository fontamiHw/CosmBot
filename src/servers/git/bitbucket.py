from atlassian import Bitbucket
import logger
from db.servers import Servers


log = logger.getLogger()
class Git(object):

    def __init__(self, config, userDb, credential):        
        self.url = credential[0][Servers.URL_POS]
        self.user = credential[0][Servers.USER_NAME_POS]
        self.pwd = credential[0][Servers.TOKEN_POS]
        self.timeout = config['timeout']
        self.project_key = config['project']
        self.repo_slug = credential[0][Servers.PROJECT_POS]
        
    def connect(self):
        self.bitbucket = Bitbucket(self.url, self.user, self.pwd, self.timeout)
        
    def get_open_pr(self):
        open_pull_requests = []

        # Retrieve the pull requests for the specified repository
        pull_requests = self.bitbucket.get_pull_requests(self.project_key, self.repo_slug, state='OPEN')
        openPr=0
        # Print the pull requests information
        for pr in pull_requests:
            # Create a new dictionary with only the specified elements
            filtered_dict = self.filter_dict(pr)
            open_pull_requests.append(filtered_dict)
            openPr += 1            
        return openPr, open_pull_requests
    
    def filter_dict(self, data):
        filtered_dict = {
            'id': data.get('id'),
            'version': data.get('version'),
            'title': data.get('title'),
            'href': data.get('links', {}).get('self', [{}])[0].get('href')
        }
        return filtered_dict
    
    def get_open_pr_from_email(self, user_mail):
        open_pull_requests = []

        # Retrieve the pull requests for the specified repository
        pull_requests = self.bitbucket.get_pull_requests(self.project_key, self.repo_slug, state='OPEN')
        openPr=0
        # Print the pull requests information
        for data in pull_requests:
            filtered_dict = {
            'email': data.get('author').get('user').get('emailAddress'),
            'name': data.get('author').get('user').get('name'),
            'id': data.get('id'),
            }
            if user_mail in filtered_dict['email']:
                # Create a new dictionary with only the specified elements
                open_pull_requests.append(filtered_dict)
                openPr += 1            
        return {"pr-numbers":openPr, "pr-list":open_pull_requests}
                