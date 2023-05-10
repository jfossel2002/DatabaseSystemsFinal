# DatabaseSystemsFinal
Simulates a database for Cabellas, and provides interfaces for interaction
Run the database_interfaces.py file (python3 database_interfaces.py)
This will run the main menu where you can select which interface you want to access
From there you can select your roll and enter sub-menus to run spefifc use-cases

Note: If you're running on Mac run the database_interfaces_mac.py, and windows run database_interfaces_windows.py
We use clear commands in the terminal to make formatting nicer, and these commands are not cross platform,
(cls for windows and clear for mac), so we made two different versions

Interface guide:
1. Customer (Ids 1-10)
    1. Online purchase (Pruchase products from online)
    2. Purchase history (See history of all purchases)
2. Store (Ids 1-4)
    1. Update Inventory (Add incoming restocks to store's inventory)
    2. Restock (Create restocks to warehouse for all low stock products)
    3. Stock (Create a restock for a product manually)
    4. Sales History (See history of all Sales)
    5. Restock History (See history of all Restocks)
    6. View Inventory Levels (View all products in stock in store and amount)
3. Warehouse (Ids 1-4)
    1. Update Warehouse Inventory (Add incoming shipments to warehouses's inventory)
    2. Reorder (Create reorders to a vendor for all low stock products)
    3. Order (Create a reorder for a product manually)
    4. View Reorder/Order History (See history of all reorders)
    5. View Inventory Levels  (View all products in warehouse in store and amount)
4. Vendor (Ids 1-10)
     1. Fufill Reorders/Create Shipments (Fufill incoming reorders from warehouses and create a coresponding shipment)
     2. View Shipment History (See history of all shipments)
5. Market-Researcger
    9 OLAP Queries (See menu for queries and write ups for detailed description)
6. Store-Register (Stores ids 1-4)
    Simulates a stores register, see writeup for detailed description
    input UPC_Codes (ex: 10001, 10002, ..., 10011)
