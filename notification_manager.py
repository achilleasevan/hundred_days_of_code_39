from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv(r"E:\Courses\Programming\100 Days of Code The Complete Python Pro Bootcamp for 2022\Pycharm Projects\39\.env")

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    pass

    def send_sms(self, price, dep_city_name, dep_iata, arr_city_name, arr_iata,outbound_date, inbound_date):
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body=f"Low price alert! Only £{price} to fly from {dep_city_name}-{dep_iata} to {arr_city_name}-{arr_iata}, from {outbound_date} to {inbound_date}.",
                            from_=os.environ.get("TWILIO_PHONE_NUMBER"),
                            to=os.environ.get("TARGET_PHONE_NUMBER")
                        )