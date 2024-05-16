import requests
import logging


class DataManager:

    def __init__(self):
        # Example endpoint: "https://api.sheety.co/token/flightPrices/sheet1"
        self.endpoint = "YOUR_SHEETY_ENDPOINT"
        self.destination_data = {}

    def get_destination_data(self):
        try:
            response = requests.get(url=self.endpoint)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            if "sheet1" in data:
                self.destination_data = data["sheet1"]
                return self.destination_data
            else:
                logging.error("Invalid API response format: 'sheet1' key not found.")
                return {}
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch destination data: {e}")
            return {}

    def update_destination_codes(self):
        try:
            for city in self.destination_data:
                if "iataCode" in city and "id" in city:
                    new_data = {"sheet1": {"price": {"iataCode": city["iataCode"]}}}
                    url = f"{self.endpoint}/{city['id']}"
                    response = requests.put(url=url, json=new_data)
                    response.raise_for_status()  # Raise an exception for bad status codes

                    # Log successful update
                    logging.info(f"Updated destination code for city ID {city['id']}")

                else:
                    logging.warning(f"Invalid city data: {city}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to update destination codes: {e}")
            if response is not None:
                logging.error(f"Response details: {response.status_code} - {response.text}")
