from webex_bot.models.response import response_from_adaptive_card
from webexteamssdk.models.cards import (AdaptiveCard, Choice, Choices, 
                                        Column, ColumnSet, FontSize,
                                        FontWeight, Text,
                                        TextBlock)
from webex_bot.formatting import quote_info, quote_danger
from webex_bot.models.command import Command
from webexteamssdk.models.cards.actions import Submit
import logger


log = logger.getLogger()
def parse_string(input_string):
    parts = input_string.split()
    
    if len(parts) < 2:
        raise ValueError("Input string must contain at least two elements: name and email.")
    
    name = parts[0]
    email = parts[1]
    
    return name, email 

    
class RegisterUser(Command):
    USER_ID="user-id"
    USER_NAME="user-name"
    USER_EMAIL="user-email"
    ADMIN="admin"
    CHOICE="admin-choice"
    CALL_BACK="admin_register_callback"
    def __init__(self, users):
        command="add user"
        super().__init__(
            command_keyword=command,
            help_message=f"{command}: add the name and email of the new user/admin.",
            chained_commands=[AdminRegisterCB(users)])

    def execute(self, message, attachment_actions, activity):
        text1 = TextBlock("Register user as admin", weight=FontWeight.BOLDER, size=FontSize.LARGE)        
        user_id_text = Text(id=RegisterUser.USER_ID, placeholder="type here the user id")
        user_name_text = Text(id=RegisterUser.USER_NAME, placeholder="type here the name of the user", maxLength=30)
        email_text = Text(id=RegisterUser.USER_EMAIL, placeholder="type here the email of the user")
        input_column = Column(items=[user_id_text, user_name_text, email_text], width=2)
        choices = [
            Choice(title="admin", value=RegisterUser.ADMIN),
        ]
        input_server = Choices(id=RegisterUser.CHOICE, choices=choices, style="expanded")
        submit = Submit(title="Register",
                        data={
                            "callback_keyword": RegisterUser.CALL_BACK})

        card = AdaptiveCard(
            body=[ColumnSet(columns=[Column(items=[text1], width=2)]),
                  ColumnSet(columns=[Column(items=[input_server], width=2)]),
                  ColumnSet(columns=[input_column]),
                  ], actions=[submit])

        return response_from_adaptive_card(card)


class AdminRegisterCB(Command):
    def __init__(self, users):
        super().__init__(
            card_callback_keyword=RegisterUser.CALL_BACK,
            delete_previous_message=True)
        self.users = users
        
    def execute(self, message, attachment_actions, activity):     
        user_id = attachment_actions.inputs.get(RegisterUser.USER_ID)
        name = attachment_actions.inputs.get(RegisterUser.USER_NAME)
        email = attachment_actions.inputs.get(RegisterUser.USER_EMAIL)
        admin = RegisterUser.ADMIN in (attachment_actions.inputs.get(RegisterUser.CHOICE))
        log.info(f"request of registration {user_id} - {name} - {email} - {admin}")   
        if not id or not name or not email:
            return quote_danger("All the text elements shall be compiled.")
        else:
            msg = self.users.register_user(user_id, name, email, admin)

        return quote_info(msg)
        

