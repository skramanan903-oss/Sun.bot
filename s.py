import requests
import json
import time
import hashlib
from datetime import datetime, timezone
import os


def generate_fyber_hash_payload(user_id, url):
    salt = "j8n5HxYA0ZVF"
    utc_now = datetime.now(timezone.utc)
    formatted_timestamp = utc_now.strftime("%Y-%m-%d %H:%M:%S")
    unix_timestamp = int(utc_now.timestamp())
    string_to_hash = f"{url}{formatted_timestamp}{salt}"
    hex_digest = hashlib.sha512(string_to_hash.encode("utf-8")).hexdigest()

    return {
        "user_id": user_id,
        "timestamp": unix_timestamp,
        "hash_value": hex_digest,
    }


def send_fairbid_request(user_id):
    # Path to the bundled JSON file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(BASE_DIR, "data", "request.json")

    try:
        with open(json_file_path, "r") as file:
            json_data = json.load(file)

        url = "https://fairbid.inner-active.mobi/simpleM2M/fyberMediation?spotId=2238156"
        headers = {"Content-Type": "application/json"}

        print("📤 Sending POST request to FairBid API...")
        response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()

        response_data = response.json()
        print(f"📄 Response data: {json.dumps(response_data, indent=2)}")

        impression_url = response_data.get("impression")
        completion_url = response_data.get("completion")

        if impression_url:
            print("\n🎯 Executing impression URL...")
            impression_response = requests.get(impression_url)
            print(f"Impression status: {impression_response.status_code}")

        time.sleep(0.5)

        if completion_url:
            print("\n🏁 Executing completion URL with hash payload...")
            completion_payload = generate_fyber_hash_payload(user_id, completion_url)
            print(f"Hash payload: {json.dumps(completion_payload, indent=2)}")

            completion_response = requests.post(
                completion_url,
                headers={"Content-Type": "application/json"},
                json=completion_payload,
            )
            print(f"Completion status: {completion_response.status_code}")
            try:
                print("Completion response:", completion_response.json())
            except ValueError:
                print("Completion response (text):", completion_response.text)

        print("\n🎉 All requests completed!")

    except FileNotFoundError:
        print(f"❌ JSON file not found at {json_file_path}")
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON in file")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    print("🚀 Starting FairBid API infinite loop...\n")
    run = 1
    while True:
        print(f"🔁 Run {run} started...")
        send_fairbid_request(user_id="Nxb9bs3rfsfOSgT8az4JHAYt1aH3")
        print(f"✅ Run {run} finished!\n")
        run += 1
        time.sleep(3)  # ⏱️ wait 3 seconds before the next run
