from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

WEARABLE_API_URLS = {
    "fitbit": "https://api.fitbit.com/1/user/-/activities/date/{date}.json",
    "garmin": "https://api.garmin.com/wellness-api/rest/activities",
    "apple_watch": "https://api.apple.com/health/activities"
}

class WearableAPIError(Exception):
    pass

def fetch_fitbit_data(date: str, access_token: str):
    url = WEARABLE_API_URLS["fitbit"].format(date=date)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise WearableAPIError("Failed to fetch data from Fitbit API")
    return response.json()

def fetch_garmin_data(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(WEARABLE_API_URLS["garmin"], headers=headers)
    if response.status_code != 200:
        raise WearableAPIError("Failed to fetch data from Garmin API")
    return response.json()

def fetch_apple_watch_data(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(WEARABLE_API_URLS["apple_watch"], headers=headers)
    if response.status_code != 200:
        raise WearableAPIError("Failed to fetch data from Apple Watch API")
    return response.json()

@router.get("/wearable/{device}/{date}")
async def get_wearable_data(device: str, date: str, access_token: str):
    try:
        if device == "fitbit":
            return fetch_fitbit_data(date, access_token)
        elif device == "garmin":
            return fetch_garmin_data(access_token)
        elif device == "apple_watch":
            return fetch_apple_watch_data(access_token)
        else:
            raise HTTPException(status_code=400, detail="Unsupported device")
    except WearableAPIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")