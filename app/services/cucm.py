# from typing import List

from zeep import Client, Transport
from zeep.exceptions import Fault

# from requests import Session
from requests.auth import HTTPBasicAuth

from app.config import config
from app.services import helpers

# from app.models import css_models

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# import logging
# logging.basicConfig(level=logging.DEBUG)


class CUCM:
    def __init__(self):
        """
        Initiate client and cucm AXL API service
        """
        transport = Transport(timeout=10)

        auth = HTTPBasicAuth(config.ucm_username, config.ucm_password)

        self.client = Client(config.wsdl, transport=transport)
        self.client.transport.session.auth = auth

        # ignore invalid certificates, required when using self signed certs
        self.client.transport.session.verify = False

        self.service = self.client.create_service(
            binding_name="{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
            address=config.ucm_url,
        )

    def get_css_list(self):
        """
        get a list of all CSS on system,and return a list of dicts
        containing the CSS Name and UUID

        Returns:
            css_list (list): List of Dicts containing CSS Name and UUIID
        """

        # search criteria % is wild card
        # if return tags not included  value returned will be null
        search_criteria = {
            "searchCriteria": {"name": "%"},
            "returnedTags": {"name": ""},
        }
        result = self.service.listCss(**search_criteria)

        # list comprehension to collect name and uuid from returned values
        css_list = [
            {"name": css["name"], "uuid": css["uuid"]}
            for css in result["return"]["css"]
        ]

        return css_list

    def get_css_detail(self, css_id):
        """
        take a CSS name or UUID and  get detailed information about the CSS
        including:
         * name,
         * uuid,
         * description,
         * partitions assigned to CSS,
         * partition UUID's

        Args:
            css_id (str): CSS Name or UUID

        Returns:
            css_detail (dict): CSS Details
        """
        # check if passed value is a valid UUID
        if helpers.is_uuid(css_id):
            # if value is a valid UUID get CSS detail by UUID
            result = self._get_css_detail_by_uuid(css_id)
        else:
            # if value is no a valid UUID get CSS detail by name
            result = self._get_css_detail_by_name(css_id)
        if "FAULT" in result:
            return result
        # TODO add error checking here, if CSS not found

        # parse out and format "interesting" information
        css = result["return"]["css"]
        css_detail = {
            "name": css["name"],
            "uuid": css["uuid"],
            "description": css["description"],
        }
        css_detail["members"] = [
            {
                "name": member["routePartitionName"]["_value_1"],
                "pt_uuid": member["routePartitionName"]["uuid"],
                "member_uuid": member["uuid"],
            }
            for member in css["members"]["member"]
        ]

        return css_detail

    def _get_css_detail_by_name(self, css_name):
        """get CSS Details by CSS Name

        Args:
            css_name (str): CSS Name

        Returns:
            [dict]: dictionary response
        """
        try:
            result = self.service.getCss(name=css_name)
        except Fault as f:
            result = {"FAULT": f}

        return result

    def _get_css_detail_by_uuid(self, css_uuid):
        """get CSS details by UUID

        Args:
            css_uuid ([str]): CSS UUID

        Returns:
            [dict]: dictionary response
        """
        try:
            result = self.service.getCss(uuid=css_uuid)
        except Fault as f:
            result = {"FAULT": f}
        return result

    def get_css_emerg_status(self):
        """
        check the CSS listed in the "emerge_block_css" list
        if the CSS contains the "emerg_block_pt" partition then PSTN
        for that CSS is blocked.

        if all the CSS in the list contain the block parition
        return status "blocked"

        if none of the  CSS in the list contain the block parition
        return status "open"

        if some of the CSS in the list contain the block parition
        return status "parital"

        in the event of a logic error return status "unknown"

        Returns:
            [dict]: Status: True/False (bool)
        """

        css_status_list = []
        blocked = 0

        for css in config.emerg_block_css:
            css_detail = self.get_css_emerg_status_detail(css)
            css_status_list.append(css_detail)
            if css_detail["pstn_blocked"]:
                blocked += 1

        if blocked == 0:
            emerg_status = {"status": "open"}
        elif blocked == len(css_status_list):
            emerg_status = {"status": "blocked"}
        elif blocked > 0 and blocked < len(css_status_list):
            emerg_status = {"status": "partial"}
        else:
            emerg_status = {"status": "unknown"}

        return emerg_status

    def get_css_emerg_status_all_detail(self):
        """
        check the CSS listed in the "emerge_block_css" list
        if the CSS contains the "emerg_block_pt" partition then PSTN
        for that CSS is blocked.

        return a list of dict that include the CSS name and block status

        Returns:
            [List]: List of Dicts: CSS name (str), block status (bool)
        """
        css_status_list = []
        for css in config.emerg_block_css:
            css_status_list.append(self.get_css_emerg_status_detail(css))
        return css_status_list

    def get_css_emerg_status_detail(self, css):
        """check status of the passed CSS (by name or UUID)
        if the CSS contains the "emerg_block_pt" partition then PSTN
        for that CSS is blocked.
        return dict with CSS Name and Block Status

        Args:
            css (str): CSS Name or UUID

        Returns:
            [dict]: name(str), pstn_blocked(bool)
        """
        css_detail = self.get_css_detail(css)
        if "FAULT" in css_detail:
            return css_detail
        block_status = False
        for member in css_detail["members"]:
            if member["name"] == config.emerg_block_pt:
                block_status = True
                break
        css_status = {"name": css, "pstn_blocked": block_status}
        return css_status

    # TODO very little difference between the lockdown and unlock functions
    # look to combine like parts
    def emerg_lockdown_all(self):
        pt = self.service.getRoutePartition(name=config.emerg_block_pt)
        pt_uuid = pt["return"]["routePartition"]["uuid"]

        result = []
        for css in config.emerg_block_css:
            css_data = self.service.getCss(name=css)
            css_uuid = css_data["return"]["css"]["uuid"]

            update_data = {
                "uuid": css_uuid,
                "addMembers": {
                    "member": [
                        {"routePartitionName": {"uuid": pt_uuid}, "index": "1"}
                    ]
                },
            }

            try:
                self.service.updateCss(**update_data)
                result.append({"SUCESS": f"{css} blocked"})
            except Fault as f:
                result.append({"ERROR": f"{css} failed: {f}"})

        return result

    def emerg_remove_lockdown_all(self):
        pt = self.service.getRoutePartition(name=config.emerg_block_pt)
        pt_uuid = pt["return"]["routePartition"]["uuid"]

        result = []
        for css in config.emerg_block_css:
            css_data = self.service.getCss(name=css)
            css_uuid = css_data["return"]["css"]["uuid"]

            update_data = {
                "uuid": css_uuid,
                "removeMembers": {
                    "member": [
                        {"routePartitionName": {"uuid": pt_uuid}, "index": "1"}
                    ]
                },
            }

            try:
                self.service.updateCss(**update_data)
                result.append({"SUCESS": f"{css} unblocked"})
            except Fault as f:
                result.append({"ERROR": f"{css} failed: {f}"})

        return result


cucm = CUCM()
