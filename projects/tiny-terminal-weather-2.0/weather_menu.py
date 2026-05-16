#!/usr/bin/env python3

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request


DEFAULT_USER_AGENT = os.environ.get(
    "WEATHER_USER_AGENT",
    "tiny-weather/1.0 (LaunchShell student project)"
)

SETTINGS_PATH = os.environ.get(
    "TINY_WEATHER_SETTINGS",
    os.path.join(os.path.dirname(__file__), "weather_settings.json")
)


def fetch_json(url):
    request_headers = {
        "Accept": "application/geo+json, application/json",
        "User-Agent": DEFAULT_USER_AGENT,
    }

    req = urllib.request.Request(url, headers=request_headers)

    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        return {}

    with open(SETTINGS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_settings(settings):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=2)
        file.write("\n")


def fetch_zip_location(zip_code):
    zip_code = re.sub(r"[^0-9]", "", zip_code or "")

    if len(zip_code) != 5:
        raise ValueError("Use a valid 5 digit US ZIP code.")

    data = fetch_json(f"https://api.zippopotam.us/us/{zip_code}")
    place = data.get("places", [{}])[0]

    return {
        "type": "zip",
        "zip_code": zip_code,
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "label": f"{place.get('place name', zip_code)}, {place.get('state abbreviation', '')}".strip(", "),
    }


def validate_coordinates(latitude, longitude):
    try:
        lat = float(latitude)
        lon = float(longitude)
    except ValueError:
        raise ValueError("Latitude and longitude must be numbers.")

    if lat < -90 or lat > 90:
        raise ValueError("Latitude must be between -90 and 90.")

    if lon < -180 or lon > 180:
        raise ValueError("Longitude must be between -180 and 180.")

    return str(lat), str(lon)


def coordinate_location(latitude, longitude):
    latitude, longitude = validate_coordinates(latitude, longitude)

    return {
        "type": "coords",
        "latitude": latitude,
        "longitude": longitude,
        "label": f"{latitude}, {longitude}",
    }


def fetch_forecast_url(latitude, longitude):
    points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    data = fetch_json(points_url)

    properties = data.get("properties", {})
    forecast_url = properties.get("forecast")

    if not forecast_url:
        raise ValueError("Weather.gov did not return a forecast URL for this location.")

    location = properties.get("relativeLocation", {}).get("properties", {})
    city = location.get("city", "")
    state = location.get("state", "")

    return forecast_url, f"{city}, {state}".strip(", ")


def fetch_forecast_periods(latitude, longitude):
    forecast_url, location_label = fetch_forecast_url(latitude, longitude)
    forecast = fetch_json(forecast_url)

    periods = forecast.get("properties", {}).get("periods", [])

    if not periods:
        raise ValueError("Weather.gov did not return forecast periods.")

    return location_label, periods


def print_forecast(location_label, periods, count):
    print()
    print(f"Weather forecast for {location_label}")
    print("=" * (21 + len(location_label)))

    for period in periods[:count]:
        name = period.get("name", "Forecast")
        temperature = period.get("temperature", "")
        unit = period.get("temperatureUnit", "")
        wind_speed = period.get("windSpeed", "")
        wind_direction = period.get("windDirection", "")
        short_forecast = period.get("shortForecast", "")
        detailed_forecast = period.get("detailedForecast", "")

        print()
        print(name)
        print("-" * len(name))
        print(f"Temp: {temperature}°{unit}")
        print(f"Wind: {wind_speed} {wind_direction}".strip())
        print(f"Short: {short_forecast}")

        if detailed_forecast:
            print(f"Details: {detailed_forecast}")

    print()


def show_forecast_for_location(location, count):
    latitude = location["latitude"]
    longitude = location["longitude"]
    fallback_label = location.get("label", f"{latitude}, {longitude}")

    location_label, periods = fetch_forecast_periods(latitude, longitude)

    if location.get("type") == "zip":
        location_label = fallback_label
    elif not location_label:
        location_label = fallback_label

    print_forecast(location_label, periods, count)


def prompt_enter():
    input("Press ENTER to return to the menu...")


def print_header():
    print()
    print("=====================================")
    print("------ Tiny Terminal Weather --------")
    print("=====================================")


def print_menu(settings):
    saved = settings.get("location", {})
    count = settings.get("count", 3)

    print()
    print("Menu:")

    if saved:
        print(f"Saved location: {saved.get('label', 'Unknown')}")
    else:
        print("Saved location: none")

    print(f"Forecast periods: {count}")
    print()
    print("1.) Show forecast for saved location")
    print("2.) Set saved location by ZIP code")
    print("3.) Set saved location by coordinates")
    print("4.) One-time ZIP code forecast")
    print("5.) One-time coordinate forecast")
    print("6.) Change number of forecast periods")
    print("7.) Show settings file path")
    print("Q.) Quit")
    print()


def set_saved_zip(settings):
    zip_code = input("Enter 5 digit US ZIP code > ").strip()
    location = fetch_zip_location(zip_code)
    settings["location"] = location
    save_settings(settings)
    print(f"Saved location: {location['label']}")


def set_saved_coordinates(settings):
    latitude = input("Latitude > ").strip()
    longitude = input("Longitude > ").strip()
    location = coordinate_location(latitude, longitude)
    settings["location"] = location
    save_settings(settings)
    print(f"Saved location: {location['label']}")


def one_time_zip(count):
    zip_code = input("Enter 5 digit US ZIP code > ").strip()
    location = fetch_zip_location(zip_code)
    show_forecast_for_location(location, count)


def one_time_coordinates(count):
    latitude = input("Latitude > ").strip()
    longitude = input("Longitude > ").strip()
    location = coordinate_location(latitude, longitude)
    show_forecast_for_location(location, count)


def change_count(settings):
    raw = input("How many forecast periods? > ").strip()

    try:
        count = int(raw)
    except ValueError:
        raise ValueError("Forecast period count must be a number.")

    if count < 1:
        raise ValueError("Forecast period count must be at least 1.")

    if count > 14:
        raise ValueError("Forecast period count should be 14 or less for this app.")

    settings["count"] = count
    save_settings(settings)
    print(f"Forecast periods set to {count}.")


def interactive_menu():
    settings = load_settings()

    while True:
        print_header()
        print_menu(settings)

        choice = input("Select Option > ").strip().lower()

        try:
            if choice == "1":
                location = settings.get("location")
                if not location:
                    print("No saved location. Set one first with option 2 or 3.")
                else:
                    show_forecast_for_location(location, settings.get("count", 3))
                prompt_enter()

            elif choice == "2":
                set_saved_zip(settings)
                settings = load_settings()
                prompt_enter()

            elif choice == "3":
                set_saved_coordinates(settings)
                settings = load_settings()
                prompt_enter()

            elif choice == "4":
                one_time_zip(settings.get("count", 3))
                prompt_enter()

            elif choice == "5":
                one_time_coordinates(settings.get("count", 3))
                prompt_enter()

            elif choice == "6":
                change_count(settings)
                settings = load_settings()
                prompt_enter()

            elif choice == "7":
                print(f"Settings file: {SETTINGS_PATH}")
                prompt_enter()

            elif choice == "q":
                print("Goodbye.")
                break

            else:
                print("Invalid option.")
                prompt_enter()

        except urllib.error.HTTPError as error:
            print(f"HTTP error: {error.code} {error.reason}")
            prompt_enter()

        except urllib.error.URLError as error:
            print(f"Network error: {error.reason}")
            prompt_enter()

        except (KeyError, ValueError, TimeoutError) as error:
            print(f"Weather lookup failed: {error}")
            prompt_enter()


def run_direct(args):
    if args.zip_code:
        location = fetch_zip_location(args.zip_code)
    elif args.coords:
        latitude, longitude = args.coords
        location = coordinate_location(latitude, longitude)
    else:
        settings = load_settings()
        location = settings.get("location")

        if not location:
            raise ValueError("No saved location. Run without arguments and set one from the menu.")

    show_forecast_for_location(location, max(args.count, 1))


def main():
    parser = argparse.ArgumentParser(
        description="Tiny terminal weather app using Weather.gov."
    )

    location = parser.add_mutually_exclusive_group()

    location.add_argument(
        "--zip",
        dest="zip_code",
        help="US ZIP code, example: 11201"
    )

    location.add_argument(
        "--coords",
        nargs=2,
        metavar=("LATITUDE", "LONGITUDE"),
        help="Latitude and longitude, example: 40.7128 -74.0060"
    )

    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=3,
        help="Number of forecast periods to print. Default: 3"
    )

    args = parser.parse_args()

    if args.zip_code or args.coords:
        try:
            run_direct(args)
        except urllib.error.HTTPError as error:
            print(f"HTTP error: {error.code} {error.reason}", file=sys.stderr)
            sys.exit(1)
        except urllib.error.URLError as error:
            print(f"Network error: {error.reason}", file=sys.stderr)
            sys.exit(1)
        except (KeyError, ValueError, TimeoutError) as error:
            print(f"Weather lookup failed: {error}", file=sys.stderr)
            sys.exit(1)
    else:
        interactive_menu()


if __name__ == "__main__":
    main()