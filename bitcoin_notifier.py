import requests
from win10toast import ToastNotifier # also need to install win32api
import pickle
import os

toaster = ToastNotifier()
bitcoin_api_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
filename = 'bitcoin_pickle'

def storeData(old_bitcoin):
    
    # initializing data to be stored in db
    db = old_bitcoin
    
    # Its important to use binary mode 
    dbfile = open(filename, 'wb')
    
    # source, destination 
    pickle.dump(db, dbfile)
    
    # close the file object
    dbfile.close()

def loadData():
    
    # for reading also binary mode is important 
    dbfile = open(filename, 'rb')
    
    # Open the pickle file Use pickle.load() to load it to a var
    old_bitcoin = pickle.load(dbfile)
    
    # close the file object
    dbfile.close()
    
    # calling the tracker objects
    tracker(old_bitcoin)

def tracker(old_bitcoin):
    
    # infinite loop to check bitcoin price
    while True:
        
        # make a get request
        response = requests.get(bitcoin_api_url)
        
        # Converts into a dictionary which allows you to access your JSON data easily within your code.
        response_json = response.json()
        
        # Bitcoin data is the first element of the list
        latest_bitcoin = response_json[0]['price_usd']

        # Make a comparison and find greater value based on pass parameter into toaster
        if float(latest_bitcoin) > float(old_bitcoin):
            toaster.show_toast("Bitcoin Price Grow",
                       "from ${:,.2f} to ${:,.2f}".format(float(old_bitcoin),float(latest_bitcoin)),
                       icon_path=None,
                       duration=10)

            # loop the toaster over some period of time
            while toaster.notification_active():
                time.sleep(0.1)

        # look for smaller value based on pass parameter into toaster
        elif float(latest_bitcoin) < float(old_bitcoin):
            toaster.show_toast("Bitcoin Price Down",
                       "from ${:,.2f} to ${:,.2f}".format(float(old_bitcoin),float(latest_bitcoin)),
                       icon_path=None,
                       duration=10)

            # loop the toaster over some period of time
            while toaster.notification_active():
                time.sleep(0.1)

        # stored latest value into old_bitcoin variable
        old_bitcoin = latest_bitcoin

        # finally stored the value into pickle file by storeData function
        storeData(old_bitcoin)
    
if __name__ == '__main__':

    # check for file existence If its not exits then call storeData function and create a file
    if not os.path.exists(filename):
        storeData(0)
    # once file is exited in working directory you can load the data into variable
    loadData()
    

