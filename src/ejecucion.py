#import json
#import datetime
from google_DriveAPI import GoogleDriveAPI
from google_DriveInventory import GoogleDriveInventory
from google_Database import Database



db = Database(host="localhost", user="root", password="root")
db.open_connection()
#db.create_database("TestIntegracion")
db.select_database("TestIntegracion") 
#db.create_table("InventarioIntegracion")

g_api= GoogleDriveAPI()
g_api.connect()

g_inventory= GoogleDriveInventory(db, g_api)
files_list= g_inventory.get_files_list()
g_inventory.inventory_files(files_list)

#db.close_connection()

