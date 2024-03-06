#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

dm = DataManager()
fs = FlightSearch()
nm = NotificationManager()

city_names = dm.get_city_names()

cities_with_iatacode = fs.get_city_code(city_names)

sheet_data = dm.get_sheet_data()

flights = []
for iata in cities_with_iatacode:
    flights.append(fs.get_flights_and_prices(iata))
    
for i in range(len(flights)):
    if flights[i].price < sheet_data[i]["lowestPrice"]:
        nm.send_sms(flights[i].price, flights[i].origin_city, flights[i].origin_airport, flights[i].destination_city, flights[i].destination_airport, flights[i].out_date, flights[i].return_date)




