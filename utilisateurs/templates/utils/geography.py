import requests
ZONE_TO_DEPARTEMENTS = {
    'val d\'oise': ['95'],
    "val d'oise": "95",
    'idf': ['75', '77', '78', '91', '92', '93', '94', '95'],
    'ile de france': ['75', '77', '78', '91', '92', '93', '94', '95'],
    'paris': ['75'],
    'france': [],
}
def get_cities_from_geo_zone(zone):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": zone,
        "format": "json",
        "addressdetails": 1,
        "limit": 50,
    }
    headers = {
        "User-Agent": "YourAppName/1.0"
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = set()
        for entry in data:
            address = entry.get("address", {})
            city = address.get("city") or address.get("town") or address.get("village") or address.get("county")
            if city:
                results.add(city)
        return list(results)
    return []
def get_department_codes(geo_zone_input):
    zone = geo_zone_input.strip().lower()
    for key, dept_codes in ZONE_TO_DEPARTEMENTS.items():
        if key in zone:
            return dept_codes
    return []