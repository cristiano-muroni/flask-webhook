from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

token = os.getenv("WHATSAPP_TOKEN")
print(token)


@app.route('/')
def index():
    return jsonify({"success": "API running 🚅"})

@app.route('/webhook', methods=['POST'])
def webhook_post():
    body = request.get_json()
    print(body) 

    if(body.object):
        if(body.entry & body.entry[0].changes & body.entry[0].changes[0] & body.entry[0].changes[0].value.messages & body.entry[0].changes[0].value.messages[0]):
            phone_number_id = body.entry[0].changes[0].value.metadata.phone_number_id
            fromW = body["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
            msg_body = body["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            
            url = "https://graph.facebook.com/v12.0/" + phone_number_id + "/messages?access_token=" + token
            json_body ={
                "messaging_product": "whatsapp",
                "to": fromW,
                "text": { body: "Ack: " + msg_body },
            }
            response = requests.get(url, headers={ "Content-Type": "application/json" }, data=json_body)
            data = data = response.json()
            return 200
        else:
            return 404        
                      
    

# Accepts GET requests at the /webhook endpoint. You need this URL to setup webhook initially.
# info on verification request payload: https://developers.facebook.com/docs/graph-api/webhooks/getting-started#verification-requests
@app.route('/webhook', methods=['GET'])
def webhook_get():
    # UPDATE YOUR VERIFY TOKEN
    # This will be the Verify Token value when you set up webhook 
    verify_token = os.getenv("VERIFY_TOKEN")
   # Parse params from the webhook verification request    
    mode = request.json.get('hub.mode')
    token = request.json.get('hub.token') 
    challenge = request.json.get('hub.challenge') 

    # Check if a token and mode were sent
    if(mode & token):
        # Check the mode and token sent are correct
        if(mode == "subscribe" & token == verify_token):
            # Respond with 200 OK and challenge token from the request
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            print("VERIFY TOKEN DO NOT MATCH")
            return 403    

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
