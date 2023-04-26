import json
import requests
# import the required MSAL for Python module(s)
from msal import ConfidentialClientApplication
# MSAL requires these values for interaction with the Microsoft identity platform.
# Get the values from Azure portal > Azure Active Directory > App registrations > $YOUR_APP_NAME.
config = {
    # Full directory URL, in the form of https://login.microsoftonline.com/<tenant_id>
    "authority": "https://login.microsoftonline.com/tenant_id",
    # 'Application (client) ID' of app registration in Azure portal - this value is a GUID
    "client_id": "Enter_the_Application_Id_Here",
    # Client secret 'Value' (not its ID) from 'Client secrets' in app registration in Azure portal
    "client_secret": "Enter_the_Client_Secret_Here"
}
# This app instance should be a long-lived instance because
# it maintains its own in-memory token cache (the default).
app = ConfidentialClientApplication(
    client_id=config["client_id"],
    authority=config["authority"],
    client_credential=config["client_secret"],
)
# First, check for a token in the cache, refreshing it if needed
result = app.acquire_token_silent(
    scopes=["https://graph.microsoft.com/.default"], account=None
)
# If no token was found in the cache or the token refresh failed, get a new one
if not result:
    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
print("Could not find a cached token, so fetching a new one.")
if "access_token" in result:
    # Get users from Microsoft Graph
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/users",
        headers={"Authorization": f'Bearer {result["access_token"]}'},
    ).json()
    print(f"Graph API call result: {json.dumps(response, indent=2)}")
else:
    print("Error encountered when requesting access token: " f"{result.get('error')}")
    print(result.get("error_description"))