import requests
import json

# 1. The address where we send our "order"
url = 'https://api.entur.io/journey-planner/v3/graphql'

# 2. This is how we identify ourselves (Entur likes to know who is asking)
headers = {
    'ET-Client-Name': 'rockslice-test-project'
}

query = """
{
  stopPlace(id: "NSR:StopPlace:31834") {
    name
    estimatedCalls(numberOfDepartures: 10) {
      expectedArrivalTime
      destinationDisplay {
        frontText
      }
      serviceJourney {
        line {
          publicCode
        }
      }
    }
  }
}
"""

# 4. We send the request to Entur
response = requests.post(url, json={'query': query}, headers=headers)

# 5. We turn the answer into a Python dictionary (like a list we can read)
data = response.json()

# 6. We find the list of departures in the "receipt"
stop_name = data['data']['stopPlace']['name']
departures = data['data']['stopPlace']['estimatedCalls']

print(f"--- Next departures from {stop_name} ---")

# 7. Loop through each bus and print it nicely
for bus in departures:
    destination = bus['destinationDisplay']['frontText']
    
    if "lyngbø" in destination.lower():
        line = bus['serviceJourney']['line']['publicCode']
        time_full = bus['expectedArrivalTime']
        time_short = time_full.split('T')[1][:5]
        
        print(f"Bus {line} to {destination} arrives at {time_short}")

