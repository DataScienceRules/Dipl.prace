import requests

page = "https://overpass-turbo.eu/"
api_script = "way (around:10,50.425793, 14.943426); (._;>;); out;"

with requests.session() as s:
    s.post(page, api_script)
