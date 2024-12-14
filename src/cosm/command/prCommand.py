import logger
import webex.webexHelper
from webex.webexHelper import get_email
from webex_bot.formatting import quote_danger, quote_info
from webex_bot.models.command import Command
from webex_bot.models.response import response_from_adaptive_card
from webexteamssdk.models.cards import (AdaptiveCard, Choice, Choices, Column,
                                        ColumnSet, FontSize, FontWeight, Text,
                                        TextBlock)
from webexteamssdk.models.cards.actions import Submit

log = logger.getLogger()


class PrRegister(Command):
    PR_ID="pr"
    LIST="list"
    REMOVE="remove"
    ALL="all"
    SUCCEED="succeed"
    CHOICE_ID="choices"
    CALL_BACK="pr_register_callback"
    
    def __init__(self, pr_db):
        command = "pr register"
        super().__init__(
            command_keyword=command,
            help_message=f"{command}: Add which pr You want to receive the status.",
            card=None,
            chained_commands=[PrRegisterCB(pr_db)])
        self.pr_db = pr_db

    def get_registered_pr(self , activity):
        """
        Retrieve and format the list of pull requests (PRs) registered by a user.

        Args:
            activity (dict): A dictionary containing activity details, which includes the user's email.

        Returns:
            str: A formatted string listing the PRs the user is registered in, including the PR name, trigger, and status.
        """
        email = get_email(activity)
        msg = "# You are registered in:\n"
        datas = self.pr_db.query_pr_details_by_email(email)
        for pr in datas:
            msg += f'- **{pr[0]}** trigger on **{pr[1]}** status\n'
        return msg

    def remove_pr(self, activity, message):
        """
        Removes pull request (PR) details associated with the given email and PR numbers.

        Args:
            activity: The activity object containing user information.
            message (str): The message containing the PR numbers to be removed. 
                           The PR numbers are expected to start from the third word in the message.

        Returns:
            str: A confirmation message indicating that the PR(s) have been removed.
        """
        email = get_email(activity)
        prs = message.split(" ")[2:]  # in first position there is "remove"
        self.pr_db.remove_pr_details_by_email_and_prs(email, prs)
        return self.get_registered_pr(activity)
    
    def execute(self, message, attachment_actions, activity):
        if message:
            if PrRegister.LIST in message :
                return self.get_registered_pr(activity)
            if PrRegister.REMOVE in message :
                return self.remove_pr(activity, message)
            else:
                return (
                    "# Accepted message are :\n"
                    "- **pr register**: a dialog is open to help to complete the request.\n"
                    "- **pr register remove <list pr number>**: remove all the requested pr from the register.\n"
                    "- **pr register list**: return the list of PRs You are registered on."
                )
            
        #tile
        text1 = TextBlock("Which Pr do You to register?", weight=FontWeight.BOLDER, size=FontSize.LARGE)  
        
        # text input
        url_text = Text(id=PrRegister.PR_ID, placeholder="type here the url of the server")      
        input_column = Column(items=[url_text], width=2)
        
        # radio selection
        choices = [
            Choice(title="Any Result", value=PrRegister.ALL),
            Choice(title="Only Succeed", value=PrRegister.SUCCEED),
        ]
        input_server = Choices(id=PrRegister.CHOICE_ID, choices=choices, style="expanded")
        submit = Submit(title="Register",
                        data={
                            "callback_keyword": PrRegister.CALL_BACK})

        card = AdaptiveCard(
            body=[ColumnSet(columns=[Column(items=[text1], width=2)]),
                  ColumnSet(columns=[Column(items=[input_server], width=2)]),
                  ColumnSet(columns=[input_column]),
                  ], actions=[submit])

        return response_from_adaptive_card(card)



class PrRegisterCB(Command):
    def __init__(self, pr_db):
        super().__init__(
            card_callback_keyword=PrRegister.CALL_BACK,
            delete_previous_message=True)
        self.pr_db=pr_db
        
    def execute(self, message, attachment_actions, activity):
        pr = attachment_actions.inputs.get(PrRegister.PR_ID)
        choice = attachment_actions.inputs.get(PrRegister.CHOICE_ID)
        if not pr :
            return quote_danger("Pr number must be insert.")
        else:
            self.pr_db.insert_pr_details(get_email(activity), pr, choice)       

        return quote_info(f"{pr} correctly registered. User will be informed at its final {choice} status.")
    


class PrStatus(Command):
    def __init__(self, parent): 
        command = "pr status"
        super().__init__(
            command_keyword=command,
            help_message=f"{command}: read status of specific pr.\n All mine if there is no specific request.",
            card=None,
        )
        self.sanity = parent


    def compose_message_pr(self, message): 
        response_message = "# PrStatus \n" 
        split = message.split(" ")
        for i in range(len(split)):
            if (len(split[i])>3):   
                prs= self.sanity.jenkins_event.get_job_data(split[i])   
                build_link = f"- {prs['lastCompletedBuild']} / {prs['lastFailedBuild']} FAILED\n"
                response_message += f"- [{prs['name']}]({prs['url']}) is {prs['color']} {build_link}"
        return response_message


    def compose_message_all(self): 
        self.sanity.collect_all_data_prs()                    
        return self.sanity.get_total_pr_message()  
            

    def execute(self, message, attachment_actions, activity):
        '''
            Register to the result of the Pr in the message.
            By default it is registered to the success Pr, 
              if user want to known also the result in case of fail has to write 
              'failed' on the message together with the pr number.
              <PR-xyz failed> 
        '''
        if not message:        
            git = self.sanity.git.get_open_pr_from_email(get_email(activity))
            prs= self.sanity.jenkins_event.get_job_data_from_git_pr(git)
            response_message = f"# Status of {len(prs)} pr(s):\n"
            for i in range(len(prs)):
                response_message += f"- [{prs[i]['name']}]({prs[i]['url']}) is {prs[i]['color']}\n"
        else:   
            if "all" in message: 
                response_message = self.compose_message_all()
            else:
                response_message = self.compose_message_pr(message)                    

        return response_message

