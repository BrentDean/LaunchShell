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
    "tiny-weather/1.0 (student project; contact: example@example.com)"
)


def fetch_json(url):
    request_headers = {
        "Accept": "application/geo+json, application/json",
        "User-Agent": DEFAULT_USER_AGENT,
    }

    req = urllib.request.Request(url, headers=request_headers)

    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_zip_location(zip_code):
    zip_code = re.sub(r"[^0-9]", "", zip_code or "")

    if len(zip_code) != 5:
        raise ValueError("Use a valid 5 digit US ZIP code.")

    data = fetch_json(f"https://api.zippopotam.us/us/{zip_code}")
    place = data.get("places", [{}])[0]

    return {
        "zip_code": zip_code,
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "label": f"{place.get('place name', zip_code)}, {place.get('state abbreviation', '')}".strip(", "),
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


def main():
    parser = argparse.ArgumentParser(
        description="Tiny terminal weather app using Weather.gov."
    )

    location = parser.add_mutually_exclusive_group(required=True)

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

    try:
        if args.zip_code:
            location_info = fetch_zip_location(args.zip_code)
            latitude = location_info["latitude"]
            longitude = location_info["longitude"]
            fallback_label = location_info["label"]
        else:
            latitude, longitude = args.coords
            fallback_label = f"{latitude}, {longitude}"

        location_label, periods = fetch_forecast_periods(latitude, longitude)

        if not location_label:
            location_label = fallback_label

        print_forecast(location_label, periods, max(args.count, 1))

    except urllib.error.HTTPError as error:
        print(f"HTTP error: {error.code} {error.reason}", file=sys.stderr)
        sys.exit(1)

    except urllib.error.URLError as error:
        print(f"Network error: {error.reason}", file=sys.stderr)
        sys.exit(1)

    except (KeyError, ValueError, TimeoutError) as error:
        print(f"Weather lookup failed: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()