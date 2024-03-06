#This class is responsible for talking to the Google Sheet.
import requests
from flight_search import FlightSearch
from dotenv import load_dotenv
import os

load_dotenv(r"E:\Courses\Programming\100 Days of Code The Complete Python Pro Bootcamp for 2022\Pycharm Projects\39\.env")

SHEETY_ENDPOINT= os.environ.get("SHEETY_ENDPOINT")
SHEETY_TOKEN= os.environ.get("SHEETY_TOKEN")
SHEETY_PUT_ENDPOINT = os.environ.get("SHEETY_PUT_ENDPOINT")

class DataManager:
    def get_city_names(self):
        post_header = {"Authorization": f"Bearer {SHEETY_TOKEN}"}
        sheety_get_response = requests.get(url=SHEETY_ENDPOINT, headers=post_header)
        sheety_get_result = sheety_get_response.json()
        city_names = []
        for i in range(len(sheety_get_result["prices"])):
            city_name = sheety_get_result["prices"][i]["city"]
            city_names.append(city_name)
        return(city_names)
            
    def get_sheet_data(self):
        post_header = {"Authorization": f"Bearer {SHEETY_TOKEN}"}
        sheety_get_data = requests.get(url=SHEETY_ENDPOINT, headers=post_header)
        sheety_get_data_result = sheety_get_data.json()
        sheet_data = sheety_get_data_result["prices"]
        return sheet_data
    
    def write_iata_code(self, cities_with_iatacode, sheet_data):
        s = requests.Session()
        for i in range(len(sheet_data)):
            sheety_put_api = f"{SHEETY_ENDPOINT}/{i+2}"
            post_header = {"Authorization": f"Bearer {SHEETY_TOKEN}"}
            data_for_sheet = {
                "price":
                    {
                    "iataCode": cities_with_iatacode[i]
                    }
                }
            s.put(url=sheety_put_api, json=data_for_sheet, headers=post_header)