from zeep.exceptions import Fault
import requests

from app.config import config
from app.services.cucm import CUCM

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CUCMEnvironment(CUCM):
    def __init__(self):
        super().__init__()
        self.pt_data = [
            {"name": "dp-allow-pt", "description": "dp automation testing"},
            {"name": "dp-block-pt", "description": "dp automation testing"},
        ]
        self.css_data = [
            {
                "name": "dp-loc1-css",
                "description": "dp automation testing",
                "members": {"member": []},
            },
            {
                "name": "dp-loc2-css",
                "description": "dp automation testing",
                "members": {"member": []},
            },
        ]

    def setup_cucm(self):
        for pt in self.pt_data:
            try:
                self.service.addRoutePartition(pt)
            except Fault as f:
                print(f"unable to add parition: {f}")

        pt = self.service.getRoutePartition(name="dp-allow-pt")
        pt_uuid = pt["return"]["routePartition"]["uuid"]
        for css in self.css_data:
            try:
                self.service.addCss(css)
            except Fault as f:
                print(f"unable to add CSS: {f}")
            css_uuid = self.service.getCss(name=css["name"])
            update_data = {
                "uuid": css_uuid["return"]["css"]["uuid"],
                "addMembers": {
                    "member": [
                        {"routePartitionName": {"uuid": pt_uuid}, "index": "2"}
                    ]
                },
            }
            try:
                self.service.updateCss(**update_data)
            except Fault as f:
                print(f"unable to add partition to CSS: {f}")

    def cleanup_cucm(self):
        for pt in self.pt_data:
            try:
                self.service.removeRoutePartition(name=pt["name"])
            except Fault as f:
                print(f"error: {f}")
        for css in self.css_data:
            try:
                self.service.removeCss(name=css["name"])
            except Fault as f:
                print(f"error {f}")
        self.client.transport.session.close()


class WebexTeamsBot:
    def __init__(self):
        self.base_url = config.wt_base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.wt_bot_token}",
        }
        self.wt_webhooks = [
            {
                "name": "Firehose Webhook",
                "targetUrl": f"{config.server}/bot/",
                "resource": "all",
                "event": "all",
                # "filter": "",  # optional
                # "secret": "",  # optional
            }
        ]

    def setup_webhooks(self):
        # create new webooks
        for webhook in self.wt_webhooks:
            self._create_webhook(webhook)

    def cleanup_webhooks(self):
        # Get List of existing webhooks
        r = self._get_webhooks()
        existing_hooks = r.json()

        # remove existing hooks
        for hook in existing_hooks["items"]:
            self._delete_webhook(hook["id"])

    def _get_webhooks(self):
        url = self.base_url + "/v1/webhooks"
        response = requests.get(url, headers=self.headers)

        return response

    def _create_webhook(self, webhook):
        url = self.base_url + "/v1/webhooks"
        response = requests.post(url, headers=self.headers, json=webhook)

        return response

    def _delete_webhook(self, webhook_id):
        url = self.base_url + "/v1/webhooks/" + webhook_id
        response = requests.delete(url, headers=self.headers)

        return response


cucm_env = CUCMEnvironment()
wt_bot = WebexTeamsBot()
