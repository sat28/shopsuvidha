from django.shortcuts import render
from .models import Business
from jsonschema import validate
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


def sanctity(input_d):
    schema = {
        "type": "object",
        "properties": {
            "business_name": {"type": "string", "maxLength": 500, "minLength": 1},
            "street_address": {"type": "string", "minLength": 5},
            "city": {"type": "string", "maxLength": 100, "minLength": 1},
            "pincode": {"type": "string", "maxLength": 10, "minLength": 1}
        },
        "required": ["business_name", "street_address", "city", "pincode"]
    }
    return validate(instance=input_d, schema=schema)


def add_business(request):
    if request.method == "POST":
        print(request.POST)
        try:
            sanctity(request.POST)
            lat_lon = get_lat_lon(request.POST["street_address"] + request.POST["city"])
            print(lat_lon)
            Business.objects.create(
                business_name=request.POST["business_name"],
                street_address=request.POST["street_address"],
                city=request.POST["city"],
                pincode=request.POST["pincode"],
                opening_time=request.POST["opening_time"],
                closing_time=request.POST["closing_time"],
                image=request.FILES["img"],
                latitude=lat_lon['lat'],
                longitude=lat_lon['lng']
            )
        except Exception:
            return render(request, 'add_business_listing/add_business.html', {"error": "Malformed Input"})
        return render(request, 'add_business_listing/add_business.html')
    else:
        return render(request, 'add_business_listing/add_business.html')
