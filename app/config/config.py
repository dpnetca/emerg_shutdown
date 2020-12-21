import os

from dotenv import load_dotenv

load_dotenv()

# CUCM Data
wsdl = os.getenv("WSDL_FILE")
ucm_username = os.getenv("UCM_USERNAME")
ucm_password = os.getenv("UCM_PASSWORD")
ucm_url = f"https://{os.getenv('UCM_PUB_ADDRESS')}:8443/axl/"

# Emergency Lockdown information
emerg_block_pt = "dp-block-pt"
emerg_block_css = ["dp-loc1-css", "dp-loc2-css"]
# emerg_allow_css = ["cos-3", "cos-4"]


# Webex Teams Bot info
wt_base_url = "https://webexapis.com"
wt_bot_token = os.getenv("WT_BOT_TOKEN")
wt_bot_id = os.getenv("WT_BOT_ID")

# mongo_db = os.getenv("MONGO_INITDB_DATABASE")
mongo_db_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
mongo_db_pass = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

# Environment
env = "dev"
server = os.getenv("SERVER_ADDRESS", "http://localhost:8000")
