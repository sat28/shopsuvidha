from django.shortcuts import render
from add_business_listing.models import Business
from math import sin, cos, sqrt, atan2, radians
import requests
from fuzzywuzzy import fuzz


def get_lat_lon(address):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    params = {'query': address, 'key': 'AIzaSyAVnGwAlW_xTCFShRFAPPuV-N3oqnvGvFM'}
    r = requests.get(url=url, params=params)
    data = r.json()

    max_ratio, result = 0, None
    for i in range(len(data['results'])):
        fuzz_r = fuzz.ratio(data['results'][i]['formatted_address'].lower(), address.lower())
        if fuzz_r > max_ratio:
            result = data['results'][i]['geometry']['location']
            max_ratio = fuzz_r
    return result


def get_business_in_radius(lat1, lon1, lat2, lon2):
    R = 6373.0 # radius of earth

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def display_listings(request):
    if request.method == 'POST':
        user_lat_lon = get_lat_lon(request.POST['address'])
        businesses = Business.objects.all()
        return_dict = []
        for business in businesses:
            distance = get_business_in_radius(user_lat_lon['lat'], user_lat_lon['lng'], business.latitude, business.longitude)
            if distance > 50:
                continue
            d = {
                    'business_name':business.business_name,
                    'opening_time':business.opening_time,
                    'closing_time':business.closing_time,
                    'street_address':business.street_address,
                    'city': business.city,
                    'pincode': business.pincode,
                    'latitude': business.latitude,
                    'longitude': business.longitude,
                    'image': business.image,
                    'distance': distance
                 }
            return_dict.append(d)
        return render(request, 'display_businesses/display.html', {'returned_businesses': return_dict})
    else:
        return render(request, 'display_businesses/display.html')
