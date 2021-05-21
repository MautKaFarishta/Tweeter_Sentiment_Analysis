import datetime
from geopy.geocoders import Nominatim
import pandas as pd

def getDate(d):
    curr = str(datetime.datetime.today()-datetime.timedelta(days=1)).split()[0]
    return curr

def getLatLong(loc_series):
    latLong = pd.DataFrame(columns = ['lat','lon'])
    geolocator = Nominatim(user_agent="OmkarKhilari")
    for location in loc_series[:100]:
        city = geolocator.geocode(location)
        if city:
            latLong.loc[len(latLong)] = [city.latitude,city.longitude]
    
    return latLong