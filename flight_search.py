import requests
from flight_data import FlightData
from datetime import *
from dotenv import load_dotenv
import os

load_dotenv(r"E:\Courses\Programming\100 Days of Code The Complete Python Pro Bootcamp for 2022\Pycharm Projects\39\.env")

TEQUILA_API_KEY= os.environ.get("TEQUILA_API_KEY")
TEQUILA_ENDPOINT = os.environ.get("TEQUILA_ENDPOINT")

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_city_code(self, city_names):
        cities_with_iatacode = []
        for name in city_names:
            tequila_header = {"apikey": TEQUILA_API_KEY}
            tequila_query = {
                "term": name,
                "location_types": "city"
            }
            tequila_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"

            tequila_response = requests.get(url=tequila_endpoint, params=tequila_query,headers=tequila_header)
            tequila_result = tequila_response.json()
            city_iata_code = tequila_result["locations"][0]['code']
            cities_with_iatacode.append(city_iata_code)
        return cities_with_iatacode
    
    def get_flights_and_prices(self, iata_code):
        tomorrow = datetime.now() + timedelta(days=1)
        six_months_from_now = datetime.now() + timedelta(days=180)

        tequila_header_outbound = {"apikey": TEQUILA_API_KEY}
        
        tequila_query_outbound = {
            "fly_from": "LON",
            "fly_to": iata_code,
            "date_from": tomorrow.strftime("%d/%m/%Y"),
            "date_to": six_months_from_now.strftime("%d/%m/%Y"),
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        tequila_endpoint_get = f"{TEQUILA_ENDPOINT}/search"

        tequila_response_outbound = requests.get(url=tequila_endpoint_get, params=tequila_query_outbound,headers=tequila_header_outbound)
        
        tequila_result = tequila_response_outbound.json()
        
        try:
            outbound_data = tequila_result['data'][0]
        except IndexError:
            print(f"No outbound direct flights found for {iata_code}.")
            return None
            
        outbound_flight_dict = {
            "price": outbound_data["price"],
            "dep_city_name": outbound_data["cityFrom"],
            "dep_iata": outbound_data["cityCodeFrom"],
            "arr_city_name": outbound_data["cityTo"],
            "arr_iata": outbound_data["cityCodeTo"],
            "outbound_date": datetime.fromtimestamp(outbound_data["route"][0]["dTimeUTC"]).strftime("%d/%m/%Y"),
        }

        tequila_header_inbound = {"apikey": TEQUILA_API_KEY}
        tequila_query_inbound = {
            "fly_from": iata_code,
            "fly_to": "LON",
            "date_from": (datetime.strptime(outbound_flight_dict["outbound_date"], "%d/%m/%Y") + timedelta(days=7)).strftime("%d/%m/%Y"),
            "date_to": (datetime.strptime(outbound_flight_dict["outbound_date"], "%d/%m/%Y") + timedelta(days=28)).strftime("%d/%m/%Y"),
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        tequila_response_inbound = requests.get(url=tequila_endpoint_get, params=tequila_query_inbound,headers=tequila_header_inbound)
        tequila_result = tequila_response_inbound.json()
        
        try:
            inbound_data = tequila_result['data'][0]
        except IndexError:
            print(f"No inbound direct flights found from {iata_code}.")
            return None

        inbound_flight_dict = {
            "price": inbound_data["price"],
            "dep_city_name": inbound_data["cityFrom"],
            "dep_iata": inbound_data["cityCodeFrom"],
            "arr_city_name": inbound_data["cityTo"],
            "arr_iata": inbound_data["cityCodeTo"],
            "inbound_date": datetime.fromtimestamp(inbound_data["route"][0]["dTimeUTC"]).strftime("%d/%m/%Y"),
        }

        total_price = outbound_flight_dict["price"] + inbound_flight_dict["price"]
        round_trip = [outbound_flight_dict, inbound_flight_dict, total_price]
        
        flight_data = FlightData(
        price=total_price,
        origin_city=round_trip[0]["dep_city_name"],
        origin_airport=round_trip[0]["dep_iata"],
        destination_city=round_trip[0]["arr_city_name"],
        destination_airport=round_trip[0]["arr_iata"],
        out_date=round_trip[0]["outbound_date"],
        return_date=round_trip[1]["inbound_date"]
        )

        return flight_data

