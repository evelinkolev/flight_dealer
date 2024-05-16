from data_manager import DataManager
from amadeus import Client


# https://github.com/amadeus4dev/amadeus-code-examples/blob/master/city_search/v1/get/Python%20SDK/city_search.py
def get_destination_code(city_name):
    AMADEUS_API_KEY = "YOUR_AMADEUS_API_KEY"
    AMADEUS_API_SECRET = "YOUR_AMADEUS_API_SECRET"

    amadeus = Client(client_id=AMADEUS_API_KEY, client_secret=AMADEUS_API_SECRET)

    response = amadeus.reference_data.locations.cities.get(keyword=city_name)
    code = response.data[0]["iataCode"]
    return code


# Fetching data from sheety api
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
print(sheet_data)

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = get_destination_code(row["city"])
    # Updating the empty iataCode fields
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

print(sheet_data)
