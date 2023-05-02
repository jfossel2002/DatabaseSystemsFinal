# database interfaces
import os
import mysql.connector
import datetime

cnx = mysql.connector.connect(user='com303ccarter2', password='cc3456cc',
                              host='136.244.224.221',
                              database='com303fpcj')


cursor = cnx.cursor()


def runMainMenu():
    os.system('cls')
    runMenu = True
    while (runMenu):
        rselection = input("""Select interface:
                1. OLAP\n
                2. Web Order\n
                3. Reorder\n
                4. Restock Store\n
                5. Vendor Shipment\n
                6. Update Inventory\n
                7. Update Warehouse Inventory\n
                8. Checkout\n
                9: Exit\n""")
        try:
            selection = int(rselection)
        except:
            input("Invalid input\n press enter to retry")
            try: 
                os.system('cls')
            except :
                 os.system('cls')
            runMainMenu()
        if ( selection<1 or selection>9): 
            input("Invalid input\n press enter to retry")
            runMainMenu()

        match (selection):
            case 1:
                OLAP()
            case 2:
                webOrder()
            case 3:
                reorder()
            case 4:
                restock()
            case 5:
                shipment()
            case 6:
                updateInventory()
            case 7:
                updateWarehouseInventory()
            case 8:
                checkout()
            case 9:
                print("Exiting")
                runMenu = False
                os.system('cls')
                break
            case _:
                input("Invalid input\n press enter to retry")
                runMainMenu()
# OLAP
def OLAP():
    os.system('cls')

    rselection = input("""Select overview:
            1. Inventory Value\n
            2. Total Product by Vendor\n
            3. Average Inventory Levels\n
            4. Top Customers\n
            5. Best Sellers\n
            """)
    try:
        selection = int(rselection)
    except:
        input("Invalid input\n press enter to retry")
        OLAP()
    
    if ( selection<1 or selection>5): 
        input("Invalid input\n press enter to retry")
        OLAP()
    os.system('cls')
    match (selection):
        case 1:
            # Total inventory value per store and region:
            query = """SELECT s.Region, s.Store_ID, SUM(i.Amount * i.Local_Price) as Total_Inventory_Value
                        FROM Store s
                        JOIN Inventory i ON s.Store_ID = i.Store_ID
                        GROUP BY s.Region, s.Store_ID
                        WITH ROLLUP;"""
            
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                for row in results:
                    if row[0] == None and row[1] == None: 
                        print("Total enteprise inventory value: " + str(row[2]).strip('(').strip(')').strip(',').strip('Decimal')+ "\n")
                    elif row[1] == None: 
                        print("Total inventory value in Region "+ getRegion(row[0]) + ": " + str(row[2]).strip('(').strip(')').strip(',').strip('Decimal'))
                    else:
                        print("Inventory value in Store " + str(row[1]) +": " + str(row[2]).strip('(').strip(')').strip(',').strip('Decimal'))
            except mysql.connector.Error as error:
                input(error + "\npress enter to continue\n")

        case 2:
            # Total products supplied by each vendor, broken down by region:
            query = """SELECT v.Region, v.Name as Vendor_Name, COUNT(DISTINCT sb.UPC_Code) as Total_Products
                    FROM Vendor v
                    JOIN Supplied_By sb ON v.Vendor_ID = sb.Vendor_ID
                    JOIN Product p ON sb.UPC_Code = p.UPC_Code
                    JOIN Warehouse_Inventory wi ON p.UPC_Code = wi.UPC_Code
                    JOIN Warehouse w ON wi.Warehouse_ID = w.Warehouse_ID
                    GROUP BY v.Region, v.Name
                    WITH ROLLUP;"""
            
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                for row in results:
                    if row[0] == None and row[1] == None: 
                        print("Total unique products in Enterprie: " + str(row[2]))
                    elif row[1] ==None:
                        print("Total unique products in Region " + str(row[0]) + ": " + str(row[2]) ) 
                    else:
                        print("Total unique products from Vendor " + str(row[1]) + " in Region " + str(row[0]) + ": " + str(row[2]))
            except mysql.connector.Error as error:
                input(error + "\npress enter to continue\n")
        case 3:
            # Average inventory levels for each product type by region:
            query = """SELECT w.Region, p.Product_Type, AVG(i.Amount) as Avg_Inventory
                        FROM Warehouse w
                        JOIN Warehouse_Inventory i ON w.Warehouse_ID = i.Warehouse_ID
                        JOIN Product p ON i.UPC_Code = p.UPC_Code
                        GROUP BY w.Region, p.Product_Type
                        WITH ROLLUP;"""
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                for row in results:
                    if row[0] == None and row[1] == None:
                        print("Average enterprise warehouse stock: " + str(row[2]).strip('Decimal'))
                    elif row[1] == None: 
                        print("Average warehouse stock in Region " + str(row[0]) + ": " + str(row[2]).strip('Decimal'))
                    else: 
                        print("Average warehouse stock of " + str(row[1]) + " in Region " + str(row[0]) + ": " + str(row[2]).strip('Decimal'))

            except mysql.connector.Error as error:
                input(error + "\npress enter to continue\n")
        case 4:
            # Top 10 customers by total sales in each region:
            query = """WITH CustomerSales AS (
                    SELECT c.Customer_ID, c.First_Name, c.Last_Name, SUM(si.Local_Price * si.Quanity) as Total_Sales,
                            RANK() OVER (ORDER BY SUM(si.Local_Price * si.Quanity) DESC) as Sales_Rank
                    FROM Store s
                    JOIN Sale sa ON s.Store_ID = sa.Store_ID
                    JOIN Sale_Item si ON sa.Sale_ID = si.Sale_ID
                    JOIN Customer c ON sa.Customer_ID = c.Customer_ID
                    GROUP BY c.Customer_ID, c.First_Name, c.Last_Name
                    )
                    SELECT * FROM CustomerSales WHERE Sales_Rank <= 10;"""
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                print("Top Customers (amount spent): ")
                for row in results:
                    print(str(row[4])+ ". " + str(row[1]) + " " + str(row[2]) + " (ID: " + str(row[0]) + ") Total purchase amount : " + str(row[3]).strip('Decimal'))
            except mysql.connector.Error as error:
                input(error + "\npress enter to continue\n")

        case 5:
            # best sellers
            query = """ WITH Sales AS (
                        SELECT s.Store_ID, p.Name, p.UPC_Code, SUM(si.Quanity) as Total_Sales,
                                ROW_NUMBER() OVER (PARTITION BY s.Store_ID ORDER BY SUM(si.Quanity) DESC) as Sales_Rank
                        FROM Store s
                        JOIN Sale sa ON s.Store_ID = sa.Store_ID
                        JOIN Sale_Item si ON sa.Sale_ID = si.Sale_ID
                        JOIN Product p ON si.UPC_Code = p.UPC_Code
                        GROUP BY s.Store_ID, p.Name, p.UPC_Code
                        )
                        SELECT * FROM Sales WHERE Sales_Rank <= 5;"""
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                print("Best Sellers by Store:")
                store = ""
                for row in results:
                    if str(row[0]) != store: 
                        store = str(row[0])
                        space = "\n Store " + store + ": \n"
                    else: 
                        space =""

                    print(space + str(row[4]) + ". " + row[1] +" (ID: " + str(row[2]) + ") " + "Quantity Sold: " + str(row[3]).strip('Decimal')  )
            except mysql.connector.Error as error:
                print(error)
                input( "\npress enter to continue\n")


    rselection = input("")
    os.system('cls')

# web orders
def webOrder():
    os.system('cls')

    login = input("input ur id to login or -1 to register: \n")
    # check in customer exists in database
    query = "SELECT * FROM Customer WHERE Customer_ID = " + login
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    if not cursor.fetchone():
        # no id
        login = register()
    query = """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0
        GROUP BY p.Name, p.UPC_Code, p.Price;
            """
    cursor.execute(query)
    avaliable_products = cursor.fetchall()
    multiPurchase(login, avaliable_products)
    # purchaseProduct(login, avaliable_products)

# Helper function to purchase a product


def purchaseProduct(login, avaliable_products):
    validSelection = False
    validAmount = False
    while ((not validSelection) or (not validAmount)):
        index = 0
        for product in avaliable_products:
            print("Product " + str(index) + ": " +
                  str(product[0]) + " Quantity Avalible: " + str(product[1]), "Price per product: " + str(product[3]))
            index += 1
        product_selection = input(
            "Enter the number corresponding to the product you want to purchase: \n")
        try:
            if (int(product_selection) > len(avaliable_products)-1 or int(product_selection) < 0):
                input("Not a valid product please press enter to try again")
                continue
            else:
                validSelection = True
        except:
            input("Not a valid product please press enter to try again")
            continue
        amount = input(
            "Enter the amount you want to purchaes: \n")
        try:
            intAmount = int(amount)
            if (intAmount > float(avaliable_products[int(product_selection)][1])):
                input("Not enough of that product avalible, Press enter to retry")
                continue
            else:
                validAmount = True
        except:
            input("Invalid amount please press enter to try again")
            continue

    # Handle to purchasing of the Product
    # Find Warehouse in region
    print("Success")
    query = "SELECT Region FROM Customer WHERE Customer_id=" + login
    cursor.execute(query)
    customerRegion = cursor.fetchall()
    query = "SELECT st.Store_ID, st.Region, p.Name, i.Amount, p.UPC_Code, p.Price FROM Inventory i JOIN Product p ON i.UPC_Code = p.UPC_Code JOIN Store st ON i.Store_ID = st.Store_ID WHERE p.UPC_Code =" + \
        str(avaliable_products[int(product_selection)][2])
    cursor.execute(query)
    allStores = cursor.fetchall()

    # Purchase from stores, starts for stores in region, then moves out of region if needed

    activePurchase = True
    # Outer array stores all, 2nd level is for each store, 3rd level is multiple products in store
    purchases = [[]]
    # Start a transaction so we can roll back if an error occurs
    cursor.execute("START TRANSACTION")
    inRegion = True
    index = 0
    allStoresInner = allStores
    usedStoreIDs = []
    try:
        while (intAmount > 0):
            for store in allStoresInner:
                if (float(store[3]) <= 0 or store[0] in usedStoreIDs):
                    continue
                if (inRegion):
                    if (customerRegion[0][0] == str(store[1])):
                        if (intAmount >= float(store[3])):
                            query = "UPDATE Inventory SET Amount = Amount -" + \
                                str(store[3]) + " WHERE store_id = " + \
                                str(store[0]) + " AND UPC_Code = " + \
                                str(store[4]) + ";"
                            cursor.execute(query)
                            # add to purchase to purchases array
                            purchases.append(
                                [str(store[0]), str(store[4]), str(store[3]), str(store[5]), str(store[2])])
                            intAmount -= int(store[3])
                            usedStoreIDs.append(int(store[0]))
                            if (intAmount <= 0):
                                break

                        else:
                            query = "UPDATE Inventory SET Amount = Amount -" + \
                                str(intAmount) + " WHERE store_id = " + \
                                str(store[0]) + " AND UPC_Code = " + \
                                str(store[4]) + ";"
                            cursor.execute(query)
                            purchases.append(
                                [str(store[0]), str(store[4]), str(intAmount), str(store[5]), str(store[2])])
                            intAmount -= intAmount
                            if (intAmount <= 0):
                                break
                    else:  # Not in the region
                        continue

                else:  # Out of region
                    if (intAmount >= float(store[3])):
                        query = "UPDATE Inventory SET Amount = Amount -" + \
                            str(store[3]) + " WHERE store_id = " + \
                            str(store[0]) + " AND UPC_Code = " + \
                            str(store[4]) + ";"
                        cursor.execute(query)
                        purchases.append(
                            [str(store[0]), str(store[4]), str(store[3]), str(store[5]), str(store[2])])
                        intAmount -= int(store[3])
                        usedStoreIDs.append(int(store[0]))
                        if (intAmount <= 0):
                            break

                    else:
                        query = "UPDATE Inventory SET Amount = Amount -" + \
                                str(intAmount) + " WHERE store_id = " + \
                                str(store[0]) + " AND UPC_Code = " + \
                            str(store[4]) + ";"
                        cursor.execute(query)
                        purchases.append(
                            [str(store[0]), str(store[4]), str(intAmount), str(store[5]), str(store[2])])
                        intAmount -= intAmount
                        if (intAmount <= 0):
                            break
            inRegion = False
            index += 1
            if (index > 1):  # Break if quanity changes during run
                break
            if (intAmount <= 0):
                break
    except mysql.connector.Error as error:
        print("Error caught on query, rolling back database")
        print("Error: ", error)
        cnx.rollback()  # Roll back
    return purchases


def multiPurchase(login, avalibleProducts):
    cursor.execute("START TRANSACTION")
    try:
        activePurchase = True
        allPurchases = [[[]]]
        while (activePurchase):
            purchase = purchaseProduct(login, avalibleProducts)
            for i in range(0, len(avalibleProducts)):
                # print(avalibleProducts[i][2])
                # print(purchase[1][1])
                if (str(avalibleProducts[i][2]) == str(purchase[1][1])):
                    avalibleProducts.pop(i)
                    break
            allPurchases.append(purchase)
            choice = input(
                "Would you like to purchase any additional products? Yes/No")
            if (choice.lower() == "no"):
                activePurchase = False
                break
        # Handle sales
        # Sort by store id
        allAllPurchases = [[]]
        allAllPurchases.pop(0)
        for purchase in allPurchases:
            for innerPurchase in purchase:
                if (innerPurchase != []):
                    allAllPurchases.append(innerPurchase)
        allAllPurchases = sorted(
            allAllPurchases, key=lambda x: x[0])  # sort purchases
        currentStoreId = -1
        currentSaleID = -1
        for purchase in allAllPurchases:  # Add to exisitng sale
            if (purchase[0] == currentStoreId):
                addSaleItem(purchase[1], purchase[2],
                            currentSaleID, purchase[3])
            else:
                # NewSale
                currentStoreId = purchase[0]
                currentSaleID = addSale(login, purchase[0])
                if (currentSaleID != -1):
                    addSaleItem(purchase[1], purchase[2],
                                currentSaleID, purchase[3])
                else:
                    print("Error in making sale, please try again")
                    cnx.rollback()
                    break
    except mysql.connector.Error as error:
        print("Error caught on query, rolling back database")
        print("Error: ", error)
        cnx.rollback()  # Roll back
    printPurchases(allAllPurchases)
    # printSales()
    cnx.commit()


def printSales():
    # Print all sales
    query = "SELECT * FROM Sale;"
    cursor.execute(query)
    allSales = cursor.fetchall()
    print("Sales:")
    for sale in allSales:
        print(sale)
    query = "SELECT * FROM Sale_Item;"
    cursor.execute(query)
    print("Sale items:")
    allSaleItems = cursor.fetchall()
    for saleItem in allSaleItems:
        print(saleItem)


def printPurchases(allPurchases):
    allAllPurchases = sorted(
        allPurchases, key=lambda x: x[1])  # sort purchases
    print("Purchase Summary: ")
    # ID, UPC, Amount, Price, Product_name
    totalProduct = 0
    currentProductUPC = int(allAllPurchases[0][1])
    for i in range(0, len(allAllPurchases)):
        if (int(allAllPurchases[i][1]) == currentProductUPC):
            totalProduct += int(allAllPurchases[i][2])
        else:
            print("Product: " + str(allAllPurchases[i-1][4]) + " Quantity: " +
                  str(totalProduct) + " Total Cost: " + str(totalProduct*int(allAllPurchases[i-1][3])))
            totalProduct = 0
            currentProductUPC = int(allAllPurchases[i][1])
            totalProduct += int(allAllPurchases[i][2])
    print("Product: " + str(allAllPurchases[len(allAllPurchases)-1][4]) + " Quantity: " +
          str(totalProduct) + " Total Cost: " + str(totalProduct*int(allAllPurchases[len(allAllPurchases)-1][3])))


def addSale(customer, store):  # Helper to add a sale to the database
    cursor.execute("START TRANSACTION")
    try:
        query = "SELECT IFNULL(MAX(Sale_ID), 0) + 1 FROM Sale;"
        cursor.execute(query)
        sale_id = int(cursor.fetchone()[0])
        query = "INSERT INTO Sale (Sale_ID, Store_ID, Customer_ID, Date) VALUES (" +\
            str(sale_id)+"," + str(store) + "," + str(customer) + ", NOW()); "
        cursor.execute(query)
        return sale_id
    except mysql.connector.Error as error:
        print("Error caught on query, rolling back database")
        print("Error: ", error)
        cnx.rollback()  # Roll back
        return -1


def addSaleItem(product_UPC, amount, SALE_ID, price):
    cursor.execute("START TRANSACTION")
    try:
        query = "SELECT IFNULL(MAX(Sale_ID), 0) + 1 FROM Sale;"
        cursor.execute(query)
        sale_id = int(cursor.fetchone()[0])
        query = "INSERT INTO Sale_Item (Sale_ID, UPC_Code, Quanity, Local_Price) VALUES (" + \
            str(SALE_ID) + "," + str(product_UPC) + "," + \
            str(amount) + "," + str(price) + "); "
        cursor.execute(query)
        return True
    except mysql.connector.Error as error:
        print("Error caught on query, rolling back database")
        print("Error: ", error)
        cnx.rollback()  # Roll back
        return False

# Inner purchases structure, (store, product_UPC, quantity)
# [[[Store1, 1, 5],[Store1, 2, 5]][[Store2, 2, 5],[Store2, 6, 3]]]


# Helper function to add a new user to the database
def register():
    os.system('cls')

    firstName = input("First Name: ")

    lastName = input("Last Name: ")

    phone = input('phone number: ')

    validRegion = False
    while validRegion == False:
        nregion = input(
            'Region:\n 1. North \n 2. South \n 3. East \n 4. West\n')
        if int(nregion) == 1:
            region = 'North'
            validRegion = True
        elif int(nregion) == 2:
            region = 'South'
            validRegion = True

        elif int(nregion) == 3:
            region = 'East'
            validRegion = True

        elif int(nregion) == 4:
            region = 'West'
            validRegion = True

        else:
            input('select a valid region\n hit enter to retry')

    uniqueID = False
    while uniqueID == False:
        customer_id = input('input a numeric customer id: ')
        query = "SELECT * FROM Customer WHERE Customer_ID = " + customer_id
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")

        if cursor.fetchone():
            # id exists
            input("id exists \n hit enter to try again")

        else:
            uniqueID = True
            insert = "INSERT INTO Customer(Customer_ID, First_Name, Last_Name, Phone_Number) Values (" + \
                customer_id+',\''+firstName+'\',\''+lastName+'\',\''+phone+'\');'

            try:
                # Start a transaction so we can roll back if an error occurs
                cursor.execute("START TRANSACTION")
                try:
                    cursor.execute(insert)
                except mysql.connector.Error as error:
                    print("Error caught on query, rolling back database")
                    print("Error: ", error)
                    cnx.rollback()  # Roll back
                    break
            except mysql.connector.Error as error:
                print(error)
                input("\npress enter to continue\n")
    cnx.commit()
    return customer_id

# restock between store and warehouse


def restock():
    os.system('cls')
    RESTOCK_AMOUNT = 10
    # Final all stores and products that need to be restocked
    # Query to find which products are low
    query = """SELECT i.Store_ID, i.UPC_Code, i.Amount, s.Region
                FROM Inventory AS i
                JOIN Store AS s ON i.Store_ID = s.Store_ID
                WHERE i.Amount <= 5;"""
    cursor.execute(query)
    restockProducts = cursor.fetchall()
    restockProducts = sorted(
        restockProducts, key=lambda x: x[0])  # sort purchases
    print("Items needing Restocking: ")
    for restock in restockProducts:
        print("Store ID: " + str(restock[0]) + " product UPC: " +
              str(restock[1]) + " quantity: " + str(restock[2]))
    input("Press Enter to restock")
    # Subtract products from warehouse_inventories
    for product in restockProducts:
        query = "UPDATE Warehouse_Inventory AS wi JOIN Warehouse AS w ON wi.Warehouse_ID = w.Warehouse_ID SET wi.Amount = wi.Amount - " + \
            str(RESTOCK_AMOUNT) + " WHERE w.Region = \'" + getRegion(product[3]) + \
            "\' AND wi.UPC_Code = " + str(product[1]) + ";"
        # Not actaully get subtracted from warehouse TODO
        cursor.execute(query)
    # Add Restock records
    currentStoreId = -1
    currentRestockID = -1
    for product in restockProducts:
        if (product[0] == currentStoreId):  # Add to exisitng restock
            addRestockItem(product[1], RESTOCK_AMOUNT,
                           currentRestockID)
        else:
            # New Restock
            currentStoreId = product[0]
            currentRestockID = addRestock(product[0], product[3])
            if (currentRestockID != -1):
                addRestockItem(product[1], RESTOCK_AMOUNT,
                               currentRestockID)
            else:
                print("Error in making restock, please try again")
                cnx.rollback()
                break
    # printRestocks() #Uncomment to display all Restock and Restock Items
    print("Restocking Complete")
    cnx.commit()


def getRegion(i):
    if (i == 1):
        return "North"
    if (i == 2):
        return "South"
    if (i == 3):
        return "East"
    if (i == 4):
        return "West"


def addRestock(store, warehouse):  # Helper to add a restock to the database
    cursor.execute("START TRANSACTION")
    try:
        now = datetime.datetime.now()
        current_hour = now.hour
        current_minute = now.minute
        query = "SELECT IFNULL(MAX(Stocking_ID), 0) + 1 FROM Restock;"
        cursor.execute(query)
        Stocking_ID = int(cursor.fetchone()[0])
        query = "INSERT INTO Restock (Stocking_ID, Store_ID, Warehouse_ID, Date, Time_Hour, Time_Minute, Restock_Status) VALUES (" +\
            str(Stocking_ID)+"," + str(store) + \
            "," + str(warehouse) + ", NOW() ," + str(current_hour) + "," +\
            str(current_minute) + ", \'Placed\'" + "); "
        cursor.execute(query)
        return Stocking_ID
    except mysql.connector.Error as error:
        print("Error caught on query, rolling back database")
        print("Error: ", error)
        cnx.rollback()  # Roll back
        return -1


# Helper to addRestockItem to Database
def addRestockItem(product_UPC, amount, STOCKING_ID):
    cursor.execute("START TRANSACTION")
    try:
        query = "SELECT IFNULL(MAX(STOCKING_ID), 0) + 1 FROM Restock;"
        cursor.execute(query)
        sale_id = int(cursor.fetchone()[0])
        query = "INSERT INTO Restock_Item (STOCKING_ID, UPC_Code, Quantity) VALUES (" + \
            str(STOCKING_ID) + "," + str(product_UPC) + "," + \
            str(amount) + "); "
        cursor.execute(query)
        return True
    except mysql.connector.Error as error:
        print("Error caught on query, rolling back database")
        print("Error: ", error)
        cnx.rollback()  # Roll back
        return False


def printRestocks():
    # Print all sales
    query = "SELECT * FROM Restock;"
    cursor.execute(query)
    allSales = cursor.fetchall()
    print("Restocks:")
    for sale in allSales:
        print(sale)
    query = "SELECT * FROM Restock_Item;"
    cursor.execute(query)
    print("Restock items:")
    allSaleItems = cursor.fetchall()
    for saleItem in allSaleItems:
        print(saleItem)

# reorder between warehouse and vendor
# create reorder req.


def reorder():
    os.system('cls')
    query = "SELECT DISTINCT Warehouse_ID FROM Warehouse"  # get all warehouse ids
    cursor.execute(query)
    warehouses = cursor.fetchall()

    for warehouse in warehouses:  # find the products that need reordering for each warehouse

        # input: store id (run to check for low stock and put in a reorder to nescessary vendor(s))
        query = """
                SELECT wi.UPC_Code, sb.Vendor_ID, wi.Amount
                FROM Warehouse_Inventory AS wi
                JOIN Supplied_By AS sb ON wi.UPC_Code = sb.UPC_Code
                JOIN Warehouse AS w ON wi.Warehouse_ID = w.Warehouse_ID
                WHERE wi.Warehouse_ID =""" + str(warehouse[0]) + " AND wi.Amount < 100;"

        cursor.execute(query)
        reorderProducts = cursor.fetchall()
        reorderProducts = sorted(
            reorderProducts, key=lambda x: x[1])  # sort products by vendor
        if len(reorderProducts) == 0:
            print("Warehouse " + str(warehouse[0]) + " is fully stocked.")
        else:
            print("Items needing Reordering: ")
            for product in reorderProducts:
                print("Warehouse ID: " + str(warehouse[0]) + " product UPC: " +
                      str(product[0]) + " quantity: " + str(product[2]) + " Vendor ID: " + str(product[1]))
            input("Press Enter to reorder")

        currVendor = -1
        reorder_id = -2
        for product in reorderProducts:
            vendorId = product[1]

            if vendorId != currVendor:
                # create new reorder, add curr product
                reorder_id = addReorder(warehouse[0], vendorId)
                currVendor = vendorId
                addReorderItem(product[0], 50, reorder_id)
                cnx.commit()
            else:
                # add to curr reorder
                addReorderItem(product[0], 50, reorder_id)
                cnx.commit()


def addReorder(warehouse_id, vendor_id):
    cursor.execute("START TRANSACTION")
    try:
        query = "SELECT IFNULL(MAX(Reorder_ID), 0) + 1 FROM Reorder;"
        cursor.execute(query)
        Reorder_ID = int(cursor.fetchone()[0])
        query = "INSERT INTO Reorder (Reorder_ID, Warehouse_ID, Vendor_ID, Reorder_Status) VALUES (" +\
            str(Reorder_ID)+"," + str(warehouse_id) + \
            "," + str(vendor_id) + ",'ORDERED'); "
        cursor.execute(query)
        return Reorder_ID
    except mysql.connector.Error as error:
        print("Error caught on query, rolling back database")
        print("Error: ", error)
        cnx.rollback()  # Roll back
        return -1


def addReorderItem(product_UPC, amount, reorder_id):
    cursor.execute("START TRANSACTION")
    try:
        query = "INSERT INTO Reorder_Item (Reorder_ID, UPC_Code, Amount) VALUES (" + \
            str(reorder_id) + "," + str(product_UPC) + "," + \
            str(amount) + "); "
        cursor.execute(query)
        # return True
    except mysql.connector.Error as error:
        print("Error caught on query, rolling back database")
        print("Error: ", error)
        cnx.rollback()  # Roll back
        # return False


def shipment():
    os.system('cls')
    query = "SELECT DISTINCT Vendor_ID FROM Vendor"  # get all vendors
    cursor.execute(query)
    vendors = cursor.fetchall()

    for vendor in vendors:  # find the products that need reordering for each warehouse
        query = "SELECT * FROM Reorder WHERE Vendor_ID =" + \
            str(vendor[0]) + " AND Reorder_Status = 'ORDERED';"
        cursor.execute(query)
        reorders = cursor.fetchall()
        for order in reorders:

            query = "SELECT * FROM Reorder_Item WHERE Reorder_ID =" + \
                str(order[0])+";"
            cursor.execute(query)
            products = cursor.fetchall()

            shipment_id = addShipment(order[2], vendor[0])
            query = "UPDATE Reorder SET Reorder_Status = 'Completed' WHERE Reorder_ID = " + \
                str(order[0]) + "; "
            cursor.execute(query)
            for product in products:
                addShipmentItem(product[1], 50, shipment_id)
                print("Vendor "+str(vendor[0]) + " shipped order " +
                      str(order[0]) + " to warehouse " + str(order[2]))
                cnx.commit()


def addShipment(warehouse, vendor):
    cursor.execute("START TRANSACTION")
    try:
        now = datetime.datetime.now()
        current_hour = now.hour
        current_minute = now.minute
        query = "SELECT IFNULL(MAX(Shipment_ID), 0) + 1 FROM Shipment;"
        cursor.execute(query)
        Shipment_ID = int(cursor.fetchone()[0])
        query = "INSERT INTO Shipment (Shipment_ID, Vendor_ID, Warehouse_ID, Shipment_Date, Time_Hour, Time_Minute, Shipment_Status) VALUES (" +\
            str(Shipment_ID)+"," + str(vendor) + \
            "," + str(warehouse) + ", NOW() ," + str(current_hour) + "," +\
            str(current_minute) + ", \'1\'" + "); "
        cursor.execute(query)
        return Shipment_ID
    except mysql.connector.Error as error:
        print("Error caught on query, rolling back database")
        print("Error: ", error)
        cnx.rollback()  # Roll back
        return -1


def addShipmentItem(product_UPC, amount, Shipment_ID):
    cursor.execute("START TRANSACTION")
    try:
        query = "INSERT INTO Shipment_Item (Shipment_ID, UPC_Code, Quantity) VALUES (" + \
            str(Shipment_ID) + "," + str(product_UPC) + "," + \
            str(amount) + "); "

        cursor.execute(query)
        return True
    except mysql.connector.Error as error:
        print("Error caught on query, rolling back database")
        print("Error: ", error)
        cnx.rollback()  # Roll back
        return False


def updateInventory():
    # Find all Pending Restocks
    os.system('cls')
    query = "SELECT * FROM Restock WHERE Restock_Status = 'Placed';"
    cursor.execute(query)
    allRestocks = cursor.fetchall()
    now = datetime.datetime.now()
    print("Restocks arrived since last check: ")
    for restock in allRestocks:
        restockHour = restock[2]
        restockMinute = restock[3]
        time_obj = datetime.time(restockHour, restockMinute)
        date_obj = datetime.datetime.combine(restock[1], time_obj)
        if (now > date_obj):
            print("ID: " + str(restock[0]) + " Store: " +
                  str(restock[5]) + " Warehouse: " + str(restock[6]))
    if (len(allRestocks) != 0):
        print("Updating store inventories...")
        for restock in allRestocks:
            query = "SELECT * FROM Restock_Item WHERE Stocking_ID = " + \
                str(restock[0]) + "; "
            cursor.execute(query)
            restockItems = cursor.fetchall()
            for item in restockItems:
                query = "UPDATE Inventory SET Amount = Amount +" + \
                    str(item[0]) + " WHERE store_id = " + \
                    str(restock[5]) + " AND UPC_Code = " + \
                    str(item[2]) + ";"
                cursor.execute(query)
            query = "UPDATE Restock SET Restock_Status = 'Completed' WHERE Stocking_ID = " + \
                str(restock[0]) + "; "
            cursor.execute(query)
        print("Updated\n")
    cnx.commit()


def updateWarehouseInventory():
    os.system('cls')
    query = "SELECT * FROM Shipment WHERE Shipment_Status = 1;"
    cursor.execute(query)
    allShipments = cursor.fetchall()
    now = datetime.datetime.now()
    print("Shipments arrived since last check: ")
    for shipment in allShipments:
        shipmentHour = shipment[2]
        shipmentMinute = shipment[3]
        time_obj = datetime.time(shipmentHour, shipmentMinute)
        date_obj = datetime.datetime.combine(shipment[1], time_obj)
        if (now > date_obj):
            print("ID: " + str(shipment[0]) + " Warehouse: " +
                  str(shipment[6]) + " Vendor: " + str(shipment[5]))
    if (len(allShipments) != 0):
        print("Updating warehouse inventories...")
        for shipment in allShipments:
            query = "SELECT * FROM Shipment_Item WHERE Shipment_ID = " + \
                str(shipment[0]) + "; "
            cursor.execute(query)
            shipmentItems = cursor.fetchall()
            for item in shipmentItems:
                query = "UPDATE Warehouse_Inventory SET Amount = Amount +" + \
                    str(item[0]) + " WHERE warehouse_id = " + \
                    str(shipment[6]) + " AND UPC_Code = " + \
                    str(item[1]) + ";"
                cursor.execute(query)
            query = "UPDATE Shipment SET Shipment_Status = 0 WHERE Shipment_ID = " + \
                str(shipment[0]) + "; "
            cursor.execute(query)
        print("Updated\n")
    cnx.commit()


# checkout - update inventory and customer frequent buys
def checkout():
    # input: customer info ,  product id and quantity , store id
    input()


def main():
    runMainMenu()


main()
