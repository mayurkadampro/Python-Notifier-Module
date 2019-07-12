# also need to install win32api
from win10toast import ToastNotifier # pip install win10toast
import urllib.request
import json
import pickle
import os

# One-time initialization
toaster = ToastNotifier()

API_KEY = "AIzaSyD4a5qZCNfXIq7j0EcOB6pbonCY7eeEyFg"
CHANNEL_ID = 'UCeVmancWx92vTZ9IPYOKnKg'
old_subs = 0
filename = 'subscriber_pickle'

def storeData(old_subs):

    # initializing data to be stored in db
    db = old_subs
    
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
    old_subs = pickle.load(dbfile)
    
    # close the file object
    dbfile.close()
    
    # calling the tracker objects
    tracker(old_subs)



def tracker(old_subs):

    # infinite loop
    while True:

        # parsing data from URL
        data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={}&key={}".format(CHANNEL_ID,API_KEY)).read()

        # load name from data field
        name = json.loads(data)["items"][0]["snippet"]["title"]

        # load sub_count from data field
        new_subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
        
        # looking for increase in sub_count
        if int(new_subs) > int(old_subs):
            toaster.show_toast("You Got New Subscriber!!!!",
                           name + " has " + "{:,d}".format(int(new_subs)) + " subscribers!",icon_path=None,duration=10)

            # loop the toaster over some period of time
            while toaster.notification_active():
                time.sleep(0.1)

        # looking for decrease in sub_count
        if int(new_subs) < int(old_subs):
            diff = old_subs - int(new_subs)
            toaster.show_toast("You Lose {} Subscriber ".format(diff),
                           name + " has " + "{:,d}".format(int(new_subs)) + " subscribers!",
                           icon_path=None,
                           duration=10)

            # loop the toaster over some period of time
            while toaster.notification_active():
                time.sleep(0.1)

        # stored latest value into old_subs variable
        old_subs = int(new_subs)

        # lastly pass the old_subs varibale in storedData function 
        storeData(old_subs)

if __name__ == '__main__':
    # check for file existence If its not exits then call storeData function and create a file
    if not os.path.exists(filename):
        storeData(0)
    # once file is exited in working directory you can load the data into variable
    loadData()
