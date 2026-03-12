import requests
import smtplib
import time
from email.mime.text import MIMEText

EMAIL = "forexbotalert@gmail.com"
PASSWORD = "xigcadybahqqiirl"
TO_EMAIL = "forexbotalert@gmail.com"

last_signal = ""

def send_email(message):
    msg = MIMEText(message)
    msg["Subject"] = "Forex Signal"
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
    server.quit()


def get_price():
    url = "https://api.exchangerate.host/latest?base=GBP&symbols=USD"
    data = requests.get(url).json()
    price = data.get("rates", {}).get("USD")

    if price is None:
        return 0

    return float(price)


while True:
    price = get_price()

    if price == 0:
        print("Price error, retrying...")
        time.sleep(60)
        continue

    if price > 1.2800:
        signal = "SELL GBPUSD"

    elif price < 1.2700:
        signal = "BUY GBPUSD"

    else:
        signal = "NO TRADE"

    global last_signal

    if signal != last_signal:

        message = f"""
Forex Signal Alert

Pair: GBPUSD
Signal: {signal}
Price: {price}
"""

        send_email(message)
        print("Signal sent:", signal)

        last_signal = signal

    time.sleep(300)
