from twilio.rest import Client 
 
account_sid = 'ACceee22f71127f717719df1ea2b7ea282' 
auth_token = '205a15d2f34ebe2718dee5a3a1cd98a6' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create(  
                              messaging_service_sid='MG74ca0ebc1271137ad5bd637158bcd292', 
                              body='ahoy from python',      
                              to='+16193811233' 
                          ) 
 
print(message.sid)