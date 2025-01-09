import requests
from bs4 import BeautifulSoup
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

geolocator = Nominatim(user_agent="event_scraper")

url = "https://www.eventbrite.de/d/germany--cologne/events"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


events = soup.find_all("div", class_="Stack_root__1ksk7")

event_list = []
for event in events:
    try:
        title_tag = event.find("a", class_="event-card-link")
        title = title_tag.text.strip() if title_tag else "Kein Titel"
        location_tag = event.find("p", class_="Typography_root__487rx #585163 Typography_body-md__487rx event-card__clamp-line--one Typography_align-match-parent__487rx")
        location = location_tag.text.strip() if location_tag else "Köln"
        date_tag = event.find("p", class_="Typography_root__487rx #3a3247 Typography_body-md-bold__487rx Typography_align-match-parent__487rx")
        date = date_tag.text.strip() if date_tag else "Kein Datum gefunden"
        link_tag = event.find("a", href=True)
        link = link_tag['href'] if link_tag else "kein Link verfügbar"

        event_list.append({
            "Titel": title,
            "Datum": date,
            "Ort": location,
            "Link": link
        })
    except AttributeError as e:
        print(f"Fehler beim Verarbeiten eines Events: {e}")

df = pd.DataFrame(event_list)
df.to_csv("koeln_events.csv", index=False)



for event in event_list:
    if event["Link"]:
        try:
            event_response = requests.get(event["Link"])
            event_soup = BeautifulSoup(event_response.content, "html.parser")

            address_container = event_soup.find("p", class_="location-info__address-text")

            if address_container and address_container.next_sibling:
               raw_address = address_container.next_sibling.strip()
               print("Extrahierte Adresse:", raw_address)
               event["Adresse"] = raw_address
            else:
                print("Adresse nicht gefunden")
                event["Adresse"] = "Adresse nicht gefunden"

            address = event["Adresse"]

            geocode_cache = {}


            address_key = address.lower()
            if address_key in geocode_cache:
                location = geocode_cache[address_key]
            else:
                try:
                    location = geolocator.geocode(f"{address}, Deutschland", timeout=10)
                    geocode_cache[address_key] = location
                except GeocoderTimedOut:
                    location = None

            if location:
                event["lat"] = location.latitude
                event["lon"] = location.longitude
                print(f"Geokodiert: {address} -> Lat: {event['lat']}, Lon: {event['lon']}")
            else:
                event["lat"], event["lon"] = None, None
                print(f"Überspringe Geokodierung für ungültige Adresse: {address}")

                time.sleep(1)
        except Exception as e:
            print(f"Fehler bei Event: {event['Titel']}, Link: {event['Link']} -> {e}")
            event["lat"], event["lon"] = None, None

map = folium.Map(location=[50.9375, 6.9603], zoom_start=12)
for event in event_list:
    lat = event.get("lat")
    lon = event.get("lon")
    adresse = event.get("Adresse", "Unbekannte Adresse")

    if lat and lon:
        folium.Marker(
            location=[lat, lon],
            popup=f"{event['Titel']}<br>{adresse}<br><a href='{event['Link']}' target='_blank'>Link</a>"
        ).add_to(map)
    else:
        print(f"Keine Koordinaten für Adresse: {adresse}")
map.save("events_map2.html")