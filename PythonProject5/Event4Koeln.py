import requests
from bs4 import BeautifulSoup
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from folium.plugins import MarkerCluster

geolocator = Nominatim(user_agent="event_scraper")

event_list = []

def scrape_eventbrite():
    url = "https://www.eventbrite.de/d/germany--cologne/events"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    events = soup.find_all("div", class_="Stack_root__1ksk7")
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

            address = location

            event_list.append({
                "Titel": title,
                "Datum": date,
                "Ort": location,
                "Link": link,
                "Adresse": address,
                "lat": None,
                "lon": None
            })

            if link != "kein Link verfügbar":
                event_response = requests.get(link)
                event_soup = BeautifulSoup(event_response.content, "html.parser")

                address_container = event_soup.find("p", class_="location-info__address-text")
                if address_container and address_container.next_sibling:
                    raw_address = address_container.next_sibling.strip()
                    print("Extrahierte Adresse:", raw_address)
                    event_list[-1]["Adresse"] = raw_address
                    event["Adresse"] = raw_address
                else:
                    print("Adresse nicht gefunden")
                    event["Adresse"] = "Adresse nicht gefunden"

        except AttributeError as e:
            print(f"Fehler beim Verarbeiten eines Events von Eventbrite: {e}")

def scrape_rausgegangen():
    url = "https://rausgegangen.de/"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    event_tiles = soup.find_all("a", class_="event-tile medium w-full")
    for tile in event_tiles:
        try:
            detail_link = "https://rausgegangen.de" + tile["href"]

            title_tag = tile.find("h4", class_="text-base text-truncate--2")
            title = title_tag.text.strip() if title_tag else "Kein Titel"

            datetime_tag = tile.find("div", class_="flex justify-between")
            datetime = datetime_tag.text.strip() if datetime_tag else "Kein Datum/Uhrzeit"

            response_detail = requests.get(detail_link)
            detail_soup = BeautifulSoup(response_detail.content, "html.parser")

            address_tags = detail_soup.find_all("span", class_="text-[#2E2D2B]")
            if address_tags and len(address_tags) >= 2:
                street = address_tags[0].text.strip()
                city = address_tags[1].text.strip()
                address = f"{street}, {city}"
            else:
                address = "Adresse nicht gefunden"

            event_list.append({
                "Titel": title,
                "Datum/Uhrzeit": datetime,
                "Adresse": address,
                "Link": detail_link,
                "lat": None,
                "lon": None
            })
            print(f"Event von Rausgegangen hinzugefügt: {title}, Adresse: {address}")


        except Exception as e:
            print(f"Fehler beim Verarbeiten eines Events von Rausgegangen: {e}")

def geocode_events():
    geocode_cache = {}
    for event in event_list:
        address = event.get("Adresse", "Adresse nicht gefunden")
        if address and address != "Adresse nicht gefunden":
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
                print(f"Überspringe Geokodierung für ungültige Adresse: {address}")
        else:
            print(f"Adresse fehlt oder ist ungültig: {address}")

def create_map():
    map = folium.Map(location=[50.9375, 6.9603], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(map)


    for event in event_list:
        lat = event.get("lat")
        lon = event.get("lon")
        adresse = event.get("Adresse", "Adresse nicht gefunden")

        if lat and lon:
            folium.Marker(
                location=[lat, lon],
                popup=f"{event['Titel']}<br>{adresse}<br><a href='{event['Link']}' target='_blank'>Link</a>"
            ).add_to(marker_cluster)
        else:
            print(f"Keine Koordinaten für Adresse: {adresse}")
    map.save("events_map3.html")

scrape_eventbrite()
scrape_rausgegangen()
geocode_events()

df = pd.DataFrame(event_list)
df.to_csv("events_combined.csv", index=False)

create_map()