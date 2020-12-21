from app.services.cucm import cucm


class FinesseGadget:
    def __init__(self):
        pass

    def get_status(self):
        status = cucm.get_css_emerg_status()
        return status


gadget = FinesseGadget()
