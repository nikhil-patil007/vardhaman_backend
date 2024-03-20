import requests
import json

# notification sending Function.
def send_notification(registerToken , messageTitle , messageBody):

    reqUrl = "https://exp.host/--/api/v2/push/send"

    headersList = {
        "Accept": "application/json",
        "Accept-encoding" : "gzip, deflate",
        "Content-Type" : "application/json",
    }

    payload = json.dumps({
        "to": registerToken,
        "sound": "default",
        "title": messageTitle,
        "body": messageBody
    })

    response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
    print(response.text)