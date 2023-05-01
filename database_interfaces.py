# database interfaces
import os
import mysql.connector

cnx = mysql.connector.connect(user='com303ccarter2', password='cc3456cc',
                              host='136.244.224.221',
                              database='com303fpcj')


cursor = cnx.cursor()


def runMainMenu():
    rselection = input("""Select interface:
            1. OLAP\n
            2. Web Order\n
            3. Reorder\n
            4. Vendor Shipment\n
            5. Update Inventory\n
            6. Checkout\n""")
    try:
        selection = int(rselection)
    except:
        input("Invalid input\n press enter to retry")
        # os.system('cls')
        runMainMenu()

    match (selection):
        case 1:
            OLAP()
        case 2:
            webOrder()
        case 3:
            reorder()
        case 4:
            vendorShipment()
        case 5:
            updateInventory()
        case 6:
            checkout()
        case _:
            input("Invalid input\n press enter to retry")
            runMainMenu()
# OLAP


def OLAP():
    # os.system('cls')
    rselection = input("""Select overview:
            1. Inventory Value\n
            2. Total Product by Vendor\n
            3. Average Inventory Levels\n
            4. Top Customers\n
            """)
    try:
        selection = int(rselection)
    except:
        input("Invalid input\n press enter to retry")
        OLAP()

    match (selection):
        case 1:
            # Total inventory value per store and region:
            query = """SELECT s.Region, s.Store_ID, SUM(i.Amount * i.Local_Price) as Total_Inventory_Value
                        FROM Store s
                        JOIN Inventory i ON s.Store_ID = i.Store_ID
                        GROUP BY s.Region, s.Store_ID
                        WITH ROLLUP;"""

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
        case 3:
            # Average inventory levels for each product type by region:
            query = """SELECT w.Region, p.Product_Type, AVG(i.Amount) as Avg_Inventory
                        FROM Warehouse w
                        JOIN Warehouse_Inventory i ON w.Warehouse_ID = i.Warehouse_ID
                        JOIN Product p ON i.UPC_Code = p.UPC_Code
                        GROUP BY w.Region, p.Product_Type
                        WITH ROLLUP;"""
        case 4:
            # Top 10 customers by total sales in each region:
            query = """WITH CustomerSalesByRegion AS (
                    SELECT s.Region, c.Customer_ID, c.First_Name, c.Last_Name, SUM(si.Local_Price * si.Quanity) as Total_Sales,
                            RANK() OVER (PARTITION BY s.Region ORDER BY SUM(si.Local_Price * si.Quanity) DESC) as Sales_Rank
                    FROM Store s
                    JOIN Sale sa ON s.Store_ID = sa.Store_ID
                    JOIN Sale_Item si ON sa.Sale_ID = si.Sale_ID
                    JOIN Customer c ON sa.Customer_ID = c.Customer_ID
                    GROUP BY s.Region, c.Customer_ID, c.First_Name, c.Last_Name
                    )
                    SELECT * FROM CustomerSalesByRegion WHERE Sales_Rank <= 10;"""

        case 5:
            # best sellers
            query = """ WITH SalesByRegion AS (
                        SELECT s.Region, p.Name, p.UPC_Code, SUM(si.Local_Price * si.Quanity) as Total_Sales,
                                ROW_NUMBER() OVER (PARTITION BY s.Region ORDER BY SUM(si.Local_Price * si.Quanity) DESC) as Sales_Rank
                        FROM Store s
                        JOIN Sale sa ON s.Store_ID = sa.Store_ID
                        JOIN Sale_Item si ON sa.Sale_ID = si.Sale_ID
                        JOIN Product p ON si.UPC_Code = p.UPC_Code
                        GROUP BY s.Region, p.Name, p.UPC_Code
                        )
                        SELECT * FROM SalesByRegion WHERE Sales_Rank <= 5;"""

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    rselection = input("")


# web orders
def webOrder():
    # input: location, products, quant (check if products are in closest store, )
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
    cnx.commit()


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
    print("")
    # os.system('cls')
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


# reorder
def reorder():
    # input: store id (run to check for low stock and put in a reorder to nescessary vendor(s))
    input()

# vendor reorder shipment


def vendorShipment():
    # input: vendor_id (run to check for request to the vendor )
    input()
# update inventory from shipment


def updateInventory():
    # input: store id ( run to check if shipments needs handling at the store )
    # return any requests
    # input: order fullfillment with shipment date
    input()

# checkout - update inventory and customer frequent buys


def checkout():
    # input: customer info ,  product id and quantity , store id
    input()


def main():
    runMainMenu()


main()
