import requests
from bs4 import BeautifulSoup
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from folium.plugins import MarkerCluster
from folium import FeatureGroup, LayerControl
from folium.plugins import Search

geolocator = Nominatim(user_agent="event_scraper")

event_list = []

def scrape_eventbrite():
    url = "https://www.eventbrite.de/d/germany--cologne/events"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    events = soup.find_all("div", class_="Stack_root__1ksk7")
    links = soup.find_all("a", class_="event-card-link")

    for event, link in zip(events, links):
        try:
            title_tag = event.find("a", class_="event-card-link")
            title = title_tag.text.strip() if title_tag else "Kein Titel"
            location_tag = event.find("p", class_="Typography_root__487rx #585163 Typography_body-md__487rx event-card__clamp-line--one Typography_align-match-parent__487rx")
            location = location_tag.text.strip() if location_tag else "Köln"
            date_tag = event.find("p", class_="Typography_root__487rx #3a3247 Typography_body-md-bold__487rx Typography_align-match-parent__487rx")
            date = date_tag.text.strip() if date_tag else "Kein Datum gefunden"
            link_tag = event.find("a", href=True)
            link_url = link_tag['href'] if link_tag else "kein Link verfügbar"
            category = link.get("data-event-category", "Sonstiges")


            event_list.append({
                "Titel": title,
                "Datum": date,
                "Ort": location,
                "Link": link_url,
                "Kategorie": category,
                "Adresse": location,
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

        except Exception as e:
            print(f"Fehler beim Verarbeiten der Kategorie: {e}")

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

def create_advanced_map():
    map = folium.Map(location=[50.9375, 6.9603], zoom_start=12)

    categories = {
        "Musik": MarkerCluster(name="Musik"),
        "Sport": MarkerCluster(name="Sport"),
        "Kultur": MarkerCluster(name="Kultur"),
        "Sonstiges": MarkerCluster(name="Sonstiges"),
    }


    for event in event_list:
        lat = event.get("lat")
        lon = event.get("lon")
        adresse = event.get("Adresse", "Adresse nicht gefunden")
        category = event.get("Kategorie", "Sonstiges")

        if lat is not None and lon is not None:
            if category not in categories:
                category = "Sonstiges"

            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(
                    f"<strong>{event['Titel']}</strong><br>{adresse}<br><a href='{event['Link']}' target='_blank'>Link</a>",
                    max_width=300
                ),
                tooltip=event['Titel']
            ).add_to(categories[category])

    for cluster in categories.values():
        map.add_child(cluster)


    map.add_child(LayerControl())

    search = Search(
        layer=folium.FeatureGroup(),
        search_label="Titel",
        placeholder="Event suchen...",
        collapsed=False
    )
    map.add_child(search)

    map.save("advanced_events_map.html")

scrape_eventbrite()
scrape_rausgegangen()
geocode_events()

df = pd.DataFrame(event_list)
df.to_csv("events_combined.csv", index=False)

create_advanced_map()