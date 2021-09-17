import requests
import datetime
import smtplib
import time

MY_LONG = 31.205824
MY_LAT = 76.173636


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_lat = float(data["iss_position"]["latitude"])
    iss_lng = float(data["iss_position"]["longitude"])

    # we can see iss if our position is within +5 or -5 degrees of the iss position
    if MY_LAT-5 <= iss_lat <= MY_LAT+5 and MY_LONG-5 <= iss_lng <= MY_LONG+5:
        return True


def is_night():

    positions = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=positions)
    response.raise_for_status()
    data = response.json()

    sunrise_time = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_time = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.datetime.now().hour

    if time_now >= sunset_time or time_now <= sunrise_time:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        print("look up!")
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login("amrinderkgglr@gmail.com", "bdate21092000")
        connection.sendmail(
            from_addr="amrinderkgglr@gmail.com",
            to_addrs="amrinderkgglr@gmail.com",
            msg="look up!"
        )
