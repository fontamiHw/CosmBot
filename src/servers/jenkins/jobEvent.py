

def process_job_event(emails, pr_data, users, trigger):    
    if pr_data:               
        for email in emails:
            if 'merged' in trigger:        
                title = "# Jenkis notify Merged !!!!!\n"
                build_link = ""
            else :
                title = "# Jenkis notify:\n"
                build_link = f"is {pr_data['color']} [{pr_data['lastCompletedBuild']}]({pr_data['lastCompletedBuildUrl']}) / [{pr_data['lastFailedBuild']} FAILED]({pr_data['lastFailedBuildUrl']})\n"
            
            if pr_data:
                response_message = f"[{pr_data['name']}]({pr_data['url']}) {build_link}"
                users.send_user_message(email, f"{title} {response_message}")