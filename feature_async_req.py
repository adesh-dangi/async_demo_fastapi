import aiohttp
import asyncio
from fastapi import Depends
from fastapi.responses import JSONResponse
import time
import keys as C
from main import get_session
import requests
from keys import FOOD_API, WEATHER_API, MUSIC_API, MAP_API
from datetime import datetime
import random

async def business_get_combined_data(session: aiohttp.ClientSession = Depends(get_session)):
    """
    Fetch data from four different APIs asynchronously, save each result in a dictionary
    as soon as the call completes, and return the combined results as a JSON response.

    If an API call fails or times out, it will be handled gracefully, and the error will be
    included in the response without affecting the other API calls.

    Time Complexity Analysis:
    - Best Case: O(max(T1, T2, T3, T4)), where T1, T2, T3, T4 are the response times of each API.
      In the best case, all APIs respond quickly and simultaneously.
    - Worst Case: O(max(T1, T2, T3, T4, Timeout)), where Timeout is the maximum allowed time for any API call.
      Even if one or more APIs fail or timeout, the function will complete within this time.

    Space Complexity: O(S1 + S2 + S3 + S4), where S1, S2, S3, S4 are the sizes of the responses or error messages.
    """
    results = {}
    start_time = time.time()
    print("start", datetime.now())

    async def fetch_and_save(url, key):
        headers = {
            'x-apihub-key': C.free_api_token,
            'x-apihub-host': "Historical-Weather-API2.allthingsdev.co",
            'x-apihub-endpoint': C.end_point_header
        }
        try:
            print("key", key, "called on ", datetime.now())
            async with session.get(url, headers=headers) as response:  # 10 second timeout
                if response.status == 200:
                    data = await response.json()
                    print(f"==>> data: {data}")
                    results[key] = {"status": "success", "data": data}
                else:
                    results[key] = {
                        "status": "error", "message": f"API returned status code {response.status}"}
            time.sleep(random.choice([1, 2, 3]))
            print("key", key, "ended on ", datetime.now())
        except asyncio.TimeoutError:
            results[key] = {"status": "error",
                            "message": "API request timed out"}
        except Exception as e:
            results[key] = {"status": "error", "message": str(e)}

    # Create tasks for each API call
    # Note: You'll need to replace 'YOUR_API_KEY' with actual API keys
    tasks = [
        # asyncio.create_task(fetch_and_save(FOOD_API, "food_list", {"apiKey": "YOUR_API_KEY", "number": 5})),
        asyncio.create_task(fetch_and_save(WEATHER_API, "weather1")),
        asyncio.create_task(fetch_and_save(WEATHER_API, "weather2")),
        asyncio.create_task(fetch_and_save(WEATHER_API, "weather3")),
        # asyncio.create_task(fetch_and_save(MUSIC_API, "music_list", {"q": "pop", "type": "track", "limit": 5})),
        # asyncio.create_task(fetch_and_save(MAP_API, "map", {"address": "1600 Amphitheatre Parkway, Mountain View, CA", "key": "YOUR_API_KEY"}))
    ]
    print("call collected ", datetime.now())
    # Wait for all tasks to complete, regardless of success or failure
    await asyncio.gather(*tasks, return_exceptions=True)
    print("call collected ended", datetime.now())
    end_time = time.time()
    execution_time = end_time - start_time

    # Add execution time and overall status to the results
    results["execution_time"] = execution_time
    results["overall_status"] = "partial_success" if any(
        result["status"] == "error" for result in results.values()) else "success"

    # Return the combined results as a JSON response
    return JSONResponse(content=results)


def busines_loop_call():
    start_time = time.time()
    results = {}
    for i in range(3):
        key = "weather_rply_"+str(i)
        url = WEATHER_API
        headers = {
            'x-apihub-key': C.free_api_token,
            'x-apihub-host': "Historical-Weather-API2.allthingsdev.co",
            'x-apihub-endpoint': C.end_point_header
        }
        response = requests.get(url, timeout=10, headers=headers)
        print(">>>", response.status_code, response)
        if response.status_code == 200:
            results[key] = response.json()
            print(f"==>> results: {results}")
        else:
            results[key] = {
                "status": "error", "message": f"API returned status code {response.status_code}"}
    end_time = time.time()
    execution_time = end_time - start_time
    results["execution_time"] = execution_time
    results["overall_status"] = "partial_success" if any(
        result["status"] == "error" for result in results.values()) else "success"
    return JSONResponse(content=results)
