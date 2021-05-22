from geopy import geocoders
import pandas as pd
import datetime
from geopy.geocoders import Nominatim
import path

# address='Pune'
geolocator = Nominatim(user_agent="OmkarKhilari")
# location = geolocator.geocode(address)
# print(location.address)
# print((location.latitude, location.longitude))

data =pd.read_csv(path.path1)

s = data['location']
for i in s[:10]:
    location = geolocator.geocode(i)
    print((location.latitude,location.longitude))