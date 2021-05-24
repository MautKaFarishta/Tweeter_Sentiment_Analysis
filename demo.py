from math import nan
from geopy import geocoders
import pandas as pd
import datetime
from geopy.geocoders import Nominatim
from collections import Counter

print('Omkar'+'\033[0m' + 'Omkar')

# data = pd.read_csv('/Users/macbookpro/Desktop/Tweeter_Sentiment_Analysis/doge_to_moon.csv')
# geolocator = Nominatim(user_agent="OmkarKhilari")
# # # address='Pune'
# # geolocator = Nominatim(user_agent="OmkarKhilari")
# # # location = geolocator.geocode(address)
# # # print(location.address)
# # # print((location.latitude, location.longitude))

# # data =pd.read_csv(path.path1)

# # s = data['location']
# # for i in s[:10]:
# #     location = geolocator.geocode(i)
# #     print((location.latitude,location.longitude))


# # print(Counter(data['location']))

# cityCount = Counter(data['location'])
# cityLatLong = {}
# cityCount = Counter(dict((k, v) for k, v in cityCount.items() if type(k)!=float))

# for ci in cityCount.most_common(3):
#     print(ci)
# p=0
# for ci in cityCount:
#     if p<5:
#         print(ci);p+=1




# for city in cityCount.most_common(2):
      
#       if city in cityLatLong:
#         pass
#       else:
#         ct = geolocator.geocode(city,timeout=None)
#         if ct:
#             cityLatLong[city] = [ct.latitude,ct.longitude]
#             print(city,ct.latitude,ct.longitude)
# latLong = pd.DataFrame(columns = ['lat','lon'])
# for loctn in cityLatLong:
#       for k in range(cityCount[loctn]):
#         latLong.loc[len(latLong)] = cityLatLong[loctn]

# print(cityLatLong,latLong)