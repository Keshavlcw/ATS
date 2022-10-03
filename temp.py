import random
from twilio.rest import Client

temp = int(input("Enter the temperate"))

if temp>98.6:

    account_sid = 'AC4f9d86095408b10077b3657cbb610b69'
    auth_token = '962199f5445187d8bcf0718b58e8d14e'
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        twiml='<Response><Say>alert high body temperature found ALERT   ALERT</Say></Response>',
        to='+919788658118',
        from_='+12058510288')
    print(call.sid)
    print("you may need some medical support")

else:
    list=["thankyou","have a nice day","go inside"]
    n = random.choice(list)
    print(n)