import requests
from win10toast import ToastNotifier # also need to install win32api

toaster = ToastNotifier()
bitcoin_api_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'


old_bitcoin = 0
while True:
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    # Bitcoin data is the first element of the list
    latest_bitcoin = response_json[0]['price_usd']

    if float(latest_bitcoin) > float(old_bitcoin):
        print("Grow price ",latest_bitcoin)
        toaster.show_toast("Bitcoin Price Grow",
                   "from {} to {}".format(old_bitcoin,latest_bitcoin),
                   icon_path=None,
                   duration=10)

        while toaster.notification_active():
            time.sleep(0.1)

    elif float(latest_bitcoin) < float(old_bitcoin):
        print("Down Price",latest_bitcoin)
        toaster.show_toast("Bitcoin Price Down",
                   "from {} to {}".format(old_bitcoin,latest_bitcoin),
                   icon_path=None,
                   duration=10)

        while toaster.notification_active():
            time.sleep(0.1)

    old_bitcoin = latest_bitcoin
    
    
    

