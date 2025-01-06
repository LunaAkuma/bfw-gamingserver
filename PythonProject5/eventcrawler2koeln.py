import requests
from bs4 import BeautifulSoup
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import re

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

            address_container = event_soup.find("div", class_="location-info__address")

            if address_container:
               address = " ".join([line.strip() for line in address_container.stripped_strings])
            else:
               address = "Adresse nicht gefunden"
            print(f"Extrahierte Adresse für {event['Titel']}: {address}")

            try:
                address = address.replace("Karte anzeigen", "").strip()
                address = re.sub(r'Show map', r'Shpw map' '',  address).strip()
                location = geolocator.geocode(f"{address}, Deutschland", timeout=10)
                if location:
                    event["lat"] = location.latitude
                    event["lon"] = location.longitude
                    print(f"Geokodiert: {address} -> Lat: {event['lat']}, Lon: {event['lon']}")
                else:
                    event["lat"], event["lon"] = None, None
                    print(f"Geokodierung fehlgeschlagen für Adresse: {address}")
            except GeocoderTimedOut:
                print(f"Geokodierung für {address} zeitüberschritten.")
                event["lat"], event["lon"] = None, None

            time.sleep(1)
        except Exception as e:
            print(f"Fehler bei Event: {event['Titel']}, Link: {event['Link']} -> {e}")
            event["Adresse"] = "Fehler"
            event["lat"], event["lon"] = None, None
    else:
        event["Adresse"] = "Kein Link verfügbar"
        event["lat"], event["lon"] = None, None

map = folium.Map(location=[50.9375, 6.9603], zoom_start=12)

for event in event_list:
    lat = event.get("lat")
    lon = event.get("lon")
    adresse = event.get("Adresse", "Adresse nicht gefunden")

    if lat and lon:
        folium.Marker(
            location=[lat, lon],
            popup=f"{event['Titel']}<br>{adresse}<br><a href='{event['Link']}' target='_blank'>Link</a>"
        ).add_to(map)
    else:
        print(f"Keine Koordinaten für Adresse: {adresse}")
map.save("events_map.html")