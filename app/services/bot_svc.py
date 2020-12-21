import requests

# from pprint import pprint

from app.config import config
from app.services.cucm import cucm
from app.services import db_svc
from app.models.bot_models import Command


class WebexTeamsBot:
    def __init__(self):
        self.url = "https://webexapis.com"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + config.wt_bot_token,
        }
        self.valid_user_email = ["webex@dpnet.ca"]  # replace with DB

        self.process_command = {
            "status": Command(
                description="Get Status",
                func=self._get_status,
            ),
            "lockdown": Command(
                description="Lockdown all CSS", func=self._set_lockdown
            ),
            "open": Command(
                description="unlock all CSS", func=self._unset_lockdown
            ),
            "details": Command(
                description="See CSS lockdown Details", func=self._get_details
            ),
            "check": Command(
                description="Check single CSS Details 'check <css-name>'",
                func=self._check_css,
                has_args=True,
            ),
            "log": Command(
                description="add message to log",
                func=self._add_log,
                has_args=True,
            ),
            "help": Command(
                description="Show Help",
                func=self._show_commands,
            ),
        }

    def process_request(self, req):
        # pprint(req)
        user = req["data"]["personEmail"]

        if not self._valid_request(user):
            return False  # TODO return what???

        message = self._get_message(req["data"]["id"])
        roomId = req["data"]["roomId"]
        command_string = message.get("text", "").lower()
        command_string = command_string.replace("emergencylockdown", "")
        command_string = command_string.strip()
        command_string = command_string.split()
        command = command_string.pop(0)
        command_to_process = self.process_command.get(command)

        if not command_to_process:
            send_message = "unrecognized command"
        elif command_to_process.has_args:
            if len(command_string) < 1:
                send_message = f"command: {command} missing arguments"
            else:
                send_message = command_to_process.func(
                    " ".join(command_string)
                )
        else:
            send_message = command_to_process.func()

        self._send_message(to=roomId, message=send_message)

    def _get_message(self, message_id):
        url = self.url + f"/v1/messages/{message_id}"
        request = requests.get(url, headers=self.headers)
        return request.json()

    def _send_message(self, to, message):
        url = self.url + "/v1/messages/"
        data = {"roomId": to, "text": message}
        res = requests.post(url, headers=self.headers, json=data)
        return res

    def _valid_request(self, user):
        # TODO if request should be processed:
        # valid user, valid room etc

        if user in self.valid_user_email:
            return True
        return False

    def _valid_user_access(self):
        # TODO add proper validation here

        return True

    def _get_status(self):
        if not self._valid_user_access():
            return False  # TODO ???
        status = cucm.get_css_emerg_status()
        message = f"Current state is {status['status']}"
        return message

    def _set_lockdown(self):
        if not self._valid_user_access():
            return False  # TODO ??
        response = cucm.emerg_lockdown_all()
        message = "lockdown initiated"
        for r in response:
            for k, v in r.items():
                message += f"\n * {k}: {v}"
        return message

    def _unset_lockdown(self):
        if not self._valid_user_access():
            return False  # TODO ??
        response = cucm.emerg_remove_lockdown_all()
        message = "lockdown cleared"
        for r in response:
            for k, v in r.items():
                message += f"\n * {k}: {v}"
        return message

    def _get_details(self):
        response = cucm.get_css_emerg_status_all_detail()
        message = "Status Details:"
        for r in response:
            message += f"\n * {r['name']}: "
            message += "Blocked" if r["pstn_blocked"] else "Open"
        return message

    def _show_commands(self):
        message = "Command List:"
        for k, v in self.process_command.items():
            message += f"\n * {k} - {v.description}"
        return message

    def _check_css(self, css):
        response = cucm.get_css_emerg_status_detail(css)
        if "FAULT" in response:
            return f"CSS '{css}' Not Found: {response['FAULT']}"
        message = f"{css} is "
        message += "Blocked" if response["pstn_blocked"] else "Open"
        return message

    def _add_log(self, msg):
        db_svc.event_log(msg)
        message = "Log Entry Added"
        return message


bot = WebexTeamsBot()
