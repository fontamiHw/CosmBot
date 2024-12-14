from webex_bot.models.command import Command
from webex_bot.models.response import response_from_adaptive_card
from webexteamssdk.models.cards import (AdaptiveCard, Choice, Choices, 
                                        Column, ColumnSet, FontSize,
                                        FontWeight, Text,
                                        TextBlock)
from webex_bot.formatting import quote_info, quote_danger
from webexteamssdk.models.cards.actions import Submit
import logger


log = logger.getLogger()
    
class RegisterServer(Command):
    USER_ID="user"
    URL_ID="url"
    TOKEN_ID="token"
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
        text1 = TextBlock("Add BOT user to the server", weight=FontWeight.BOLDER, size=FontSize.LARGE)        
        url_text = Text(id=RegisterServer.URL_ID, placeholder="type here the url of the server")
        jobs_text = Text(id=RegisterServer.PROJECT, placeholder="the sub path for list of jobs (view/change-requests)")
        user_text = Text(id=RegisterServer.USER_ID, placeholder="type here the username", maxLength=30)
        token_text = Text(id=RegisterServer.TOKEN_ID, placeholder="type here the token")
        input_column = Column(items=[url_text, jobs_text, user_text, token_text], width=2)
        choices = [
            Choice(title="Git Server", value=RegisterServer.GIT),
            Choice(title="Jenkins Server", value=RegisterServer.JENKINS)
        ]
        input_server = Choices(id=RegisterServer.SERVER_ID, choices=choices, style="expanded")
        submit = Submit(title="Register",
                        data={
                            "callback_keyword": RegisterServer.CALL_BACK})

        card = AdaptiveCard(
            body=[ColumnSet(columns=[Column(items=[text1], width=2)]),
                  ColumnSet(columns=[Column(items=[input_server], width=2)]),
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
        path = attachment_actions.inputs.get(RegisterServer.PROJECT)
        user = attachment_actions.inputs.get(RegisterServer.USER_ID)
        token = attachment_actions.inputs.get(RegisterServer.TOKEN_ID)
        server = attachment_actions.inputs.get(RegisterServer.SERVER_ID)
        if not url or not user or not token or not server:
            return quote_danger("All the elements shall be compiled.")
        else:
            if self.users.is_admin(user):
                try:
                    self.users.register_in_server(server, url, path, user, token)
                except Exception as e:
                    msg = f"Coud not possible to use {user} for {server}."
                    log.error(f"{msg} : {e}")
                    return quote_danger(msg)
            else:
                return quote_danger("User {user} is not admin.")

        return quote_info(f"{user} correctly added in the dataBase. If {url} or token are wrong for {server} is not now validate.")

