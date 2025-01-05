from webex_bot.models.command import Command
from webex_bot.models.response import response_from_adaptive_card
from webexteamssdk.models.cards import (AdaptiveCard, Choice, Choices, 
                                        Column, ColumnSet, FontSize,
                                        FontWeight, Text,
                                        TextBlock)
from webex_bot.formatting import quote_info, quote_danger
from webexteamssdk.models.cards.actions import Submit
import logger
from cosmException import CosmException
from datetime import datetime, timedelta


log = logger.getLogger("commandAdmin")
    
class RegisterServer(Command):
    USER_ID="user"
    URL_ID="url"
    TOKEN_ID="token"
    TOKEN_DURATION="token_duration"
    SERVER_ID="server_choice"
    GIT="git"
    JENKINS="jenkins"
    PROJECT="project"
    CALL_BACK="server_register_callback"
    
    def __init__(self, users): 
        command="server config"
        super().__init__(
            command_keyword=command,
            help_message=f"{command}: config the git/jenkins server to the bot.",
            chained_commands=[ServerRegisterCB(users)])

    def execute(self, message, attachment_actions, activity):
        text1 = TextBlock("Add new admin to the server.", weight=FontWeight.BOLDER, size=FontSize.LARGE)        
        text1_2 = TextBlock("    (all fields are mandatory)", size=FontSize.DEFAULT, isSubtle=True)        
        text2 = TextBlock("Edit admin data.", weight=FontWeight.BOLDER, size=FontSize.LARGE)  
        text2_2 = TextBlock("    (server and username are mandatory)", size=FontSize.DEFAULT, isSubtle=True)   
        text_column1 = Column(items=[text1, text1_2])      
        text_column2 = Column(items=[text2, text2_2], separator=True)      
        
        url_text = Text(id=RegisterServer.URL_ID, placeholder="type here the url of the server")
        jobs_text = Text(id=RegisterServer.PROJECT, placeholder="the sub path for list of jobs (view/change-requests)")
        user_text = Text(id=RegisterServer.USER_ID, placeholder="type here the username", maxLength=30)
        token_text = Text(id=RegisterServer.TOKEN_ID, placeholder="type here the token")
        token_duration_text = Text(id=RegisterServer.TOKEN_DURATION, placeholder="type here the token duration time in days", value="30")
        input_column = Column(items=[url_text, jobs_text, user_text, token_text, token_duration_text], width=2)
        
        choices = [
            Choice(title="Git Server", value=RegisterServer.GIT),
            Choice(title="Jenkins Server", value=RegisterServer.JENKINS)
        ]
        input_server = Choices(id=RegisterServer.SERVER_ID, choices=choices, style="expanded")
        submit = Submit(title="Register",
                        data={
                            "callback_keyword": RegisterServer.CALL_BACK})

        card = AdaptiveCard(
            body=[ColumnSet(columns=[Column(items=[text_column1])]),
                  ColumnSet(columns=[Column(items=[text_column2])]),
                  ColumnSet(columns=[Column(items=[input_server])]),
                  ColumnSet(columns=[input_column]),
                  ], actions=[submit])

        return response_from_adaptive_card(card)


class ServerRegisterCB(Command):
    def __init__(self, users):
        super().__init__(
            card_callback_keyword=RegisterServer.CALL_BACK,
            delete_previous_message=True)
        self.users = users
        
    def execute(self, message, attachment_actions, activity):
        url = attachment_actions.inputs.get(RegisterServer.URL_ID)
        project = attachment_actions.inputs.get(RegisterServer.PROJECT)
        user = attachment_actions.inputs.get(RegisterServer.USER_ID)
        token = attachment_actions.inputs.get(RegisterServer.TOKEN_ID)
        # calculate expiration date
        token_duration = attachment_actions.inputs.get(RegisterServer.TOKEN_DURATION)
        try:
            token_duration_days = int(token_duration)
        except ValueError:
            return quote_danger("Token duration must be an integer.")
        expiration_date = datetime.now() + timedelta(days=token_duration_days)
        
        log.info(f"Token for {user} will expire on {expiration_date}")
        server = attachment_actions.inputs.get(RegisterServer.SERVER_ID)
        log.info(f"Executing command for {user} in {server} with url {url} and project {project}")
        if not user or not type:
            return quote_danger("server type and User are mandatory.")
        else:
            if self.users.is_admin(user):
                try:
                    self.users.register_in_server(server, url, project, user, token, expiration_date)
                except CosmException as e:
                    msg = e.message
                    log.error(msg)
                    return quote_danger(msg)
                except Exception as e:
                    msg = f"Could not possible to use {user} for {server}."
                    log.error(f"{msg} : {e}")
                    return quote_danger(msg)
            else:
                return quote_danger(f"User {user} is not admin.")

        return quote_info(f"{user} correctly added in the dataBase. If {url} or token are wrong for {server}, it is not yet validate.")

