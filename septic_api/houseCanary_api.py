from django.db.models.fields import NullBooleanField
import requests
import json
from django.conf import settings

print(settings.DEBUG)

def make_request(params):
    # Hardcoding this for now since I have to mock the result. 
    # Normally I'd suggest storing this somewhere else so that we could conditionally configure it for the environment or update it easily
    url = 'https://api.housecanary.com/v2/property/geocode'

    response = requests.get(url, params=params, auth=('API_KEY', 'API_SECRET'))
    # Since I know I cannot access HouseCanary make some fake json to handle. 
    # Make this conditional on the DEBUG status to keep it simple. 
    # Normally might suggest setting up .env files for each dev environment.
    #I did it this way so you could *actually* interact with the API without errors.
    if (settings.DEBUG):
        response_json = get_fake_respone(params['zipcode'])
    else:
        response_json = response.json()
    
    return response_json

def get_septic(request):
    # https://api-docs.housecanary.com/?python#levels-and-identifiers
    # The HouseCanary docs above say they need the street address and either a zipcode or the city and state. 
    # I have decided to go with zipcode just to keep it simple. 
    # In a larger project you might want to use some sort of field validation call here to another API to normalize
    # the address or to check that it exists.
    params = {
        'address': request['address'],
        'zipcode': request['zipcode'],
        }
    response_json=make_request(params)
    septic_str = json.loads(response_json)['property/details']['result']['property']['sewer']
    if septic_str == 'Septic':
        return True
    elif septic_str == 'None':
        return None
    else:
        return False

def get_fake_respone(zipcode):
    sewer_options = ['Municipal', 'None', 'Storm', 'Septic', 'Yes']
    return json.dumps({
        "property/details": {
            "api_code_description": "ok",
            "api_code": 0,
            "result": {
                "property": {
                    "air_conditioning": "yes",
                    "attic": False,
                    "basement": "full_basement",
                    "building_area_sq_ft": 1824,
                    "building_condition_score": 5,
                    "building_quality_score": 3,
                    "construction_type": "Wood",
                    "exterior_walls": "wood_siding",
                    "fireplace": False,
                    "full_bath_count": 2,
                    "garage_parking_of_cars": 1,
                    "garage_type_parking": "underground_basement",
                    "heating": "forced_air_unit",
                    "heating_fuel_type": "gas",
                    "no_of_buildings": 1,
                    "no_of_stories": 2,
                    "number_of_bedrooms": 4,
                    "number_of_units": 1,
                    "partial_bath_count": 1,
                    "pool": True,
                    "property_type": "Single Family Residential",
                    "roof_cover": "Asphalt",
                    "roof_type": "Wood truss",
                    "site_area_acres": 0.119,
                    "style": "colonial",
                    "total_bath_count": 2.5,
                    "total_number_of_rooms": 7,
                    "sewer": sewer_options[int(zipcode)%4], #Uses the provided zipcode to dynamically change provided sewer type
                    "subdivision" : "CITY LAND ASSOCIATION",
                    "water": "municipal",
                    "year_built": 1957,
                    "zoning": "RH1"
                },
                "assessment":{
                    "apn": "0000 -1111",
                    "assessment_year": 2015,
                    "tax_year": 2015,
                    "total_assessed_value": 1300000.0,
                    "tax_amount": 15199.86
                }
            }
        }
    })