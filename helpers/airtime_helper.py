import africastalking

username = "sandbox"
api_key = "fe9662a249bf505d6f7f98963a505aeab42e0936f1a53f6a2fceba16a6c820d7"

africastalking.initialize(username, api_key)

airtime = africastalking.Airtime

def send_airtime(unit, number):
    phone_number = number
    currency_code = "NGN"
    amount = unit

    try:
        response = airtime.send(phone_number=phone_number, amount=amount, currency_code=currency_code)
        print(response)
    except Exception as e:
        print(f"Encountered an error while sending airtime. More error details below\n {e}")


