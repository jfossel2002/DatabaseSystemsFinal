# database interfaces
import os
import mysql.connector
import datetime

cnx = mysql.connector.connect(
    user="com303ccarter2",
    password="cc3456cc",
    host="136.244.224.221",
    database="com303fpcj",
)


cursor = cnx.cursor()


def customerMenu():
    os.system("cls")
    runMenu = True
    while runMenu:
        first_selection = input(
            """Select Interface:\n
        1. Online Purchase\n
        2. Purchase History\n
        3. Exit
        """
        )
        try:
            fselection = int(first_selection)
        except:
            input("Invalid input\n press enter to retry")
            try:
                os.system("cls")
            except:
                os.system("cls")
            continue
        if fselection < 1 or fselection > 3:
            input("Invalid input\n press enter to retry")
            continue
        match (fselection):
            case 1:
                webOrder()
            case 2:
                purchaseHistory()
            case 3:
                print("Exiting")
                runMenu = False
                os.system("cls")
                break
            case _:
                input("Invalid input\n press enter to retry")
                continue


def StoreMenu():
    os.system("cls")
    runMenu = True
    while runMenu:
        first_selection = input(
            """Select Interface:\n
        1. Update Inventory\n
        2. Restock\n
        3. Stock\n
        4. Sales History\n
        5. Restock History\n
        6. View Inventory Levels\n
        7. Exit
        """
        )
        try:
            fselection = int(first_selection)
        except:
            input("Invalid input\n press enter to retry")
            try:
                os.system("cls")
            except:
                os.system("cls")
            continue
        if fselection < 1 or fselection > 7:
            input("Invalid input\n press enter to retry")
            continue
        match (fselection):
            case 1:
                updateInventory()
            case 2:
                restock()
            case 3:
                stock()
            case 4:
                salesHistory()
            case 5:
                restockHistory()
            case 6:
                InventoryLevels()
            case 7:
                print("Exiting")
                runMenu = False
                os.system("cls")
                break
            case _:
                input("Invalid input\n press enter to retry")
                continue


def restockHistory():
    # store login
    os.system("cls")
    store_id = input("Input Store ID: ")
    query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        store_id = input("Input Valid Store ID: ")
        query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")
    query = (
        """
    SELECT
    *
FROM Restock AS s
JOIN Restock_Item AS si ON s.Stocking_ID = si.Stocking_ID
JOIN Product AS p ON si.UPC_Code = p.UPC_Code
WHERE s.Store_ID = """
        + store_id
        + " ORDER BY s.Date DESC, s.Time_Hour DESC, s.Time_Minute DESC;"
    )
    cursor.execute(query)
    restocks = cursor.fetchall()
    print("Stores: " + str(store_id) + "'s restock history")
    for restock in restocks:
        formatted_date = restock[1].strftime("%B %d, %Y")
        print(
            formatted_date
            + " "
            + str(restock[2])
            + ":"
            + str(restock[3])
            + " Restock ID: "
            + str(restock[0])
            + " Status: "
            + str(restock[4])
            + " Warehouse ID: "
            + str(restock[5])
            + " Product: ("
            + str(restock[10])
            + ") "
            + restock[11]
            + " Quantity: "
            + str(restock[7])
        )
    input("Enter to Contiune")


def InventoryLevels():
    # store login
    os.system("cls")
    store_id = input("Input Store ID: ")
    query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        store_id = input("Input Valid Store ID: ")
        query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")
    query = (
        "SELECT * FROM Inventory as i JOIN Product as p ON i.UPC_Code = p.UPC_Code where i.Store_ID = "
        + store_id
        + " ORDER BY i.Amount DESC"
    )
    cursor.execute(query)
    inventory = cursor.fetchall()
    print("Stores: " + str(store_id) + "'s Inventory Level:")
    for item in inventory:
        print(
            "Product: ("
            + str(item[5])
            + ") "
            + item[6]
            + " Amount: "
            + str(item[0])
            + " Max Capacity: "
            + str(item[2])
            + " Price: $"
            + str(item[1])
        )
    input("Enter to Contiune")


def WarehouseMenu():
    os.system("cls")
    runMenu = True
    while runMenu:
        first_selection = input(
            """Select Interface:\n
        1. Update Warehouse Inventory\n
        2. Reorder\n
        3. Order\n
        4. View Reorder/Order History\n
        5. View Inventory Levels\n
        6. Exit
        """
        )
        try:
            fselection = int(first_selection)
        except:
            input("Invalid input\n press enter to retry")
            try:
                os.system("cls")
            except:
                os.system("cls")
            continue
        if fselection < 1 or fselection > 6:
            input("Invalid input\n press enter to retry")
            continue
        match (fselection):
            case 1:
                updateWarehouseInventory()
            case 2:
                reorder()
            case 3:
                order()
            case 4:
                reorderHistory()
            case 5:
                WarehouseInventoryLevels()
            case 6:
                print("Exiting")
                runMenu = False
                os.system("cls")
                break
            case _:
                input("Invalid input\n press enter to retry")
                continue


def reorderHistory():
    # warehouse login
    os.system("cls")
    warehouse_id = input("Input Warehouse ID: ")
    query = "SELECT * FROM Warehouse WHERE Warehouse_ID =" + warehouse_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        warehouse_id = input("Input Valid Warehouse ID: ")
        query = "SELECT * FROM Warehouse WHERE Warehouse_ID =" + warehouse_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")
    query = (
        """
    SELECT *
    FROM Reorder AS s
    JOIN Reorder_Item AS si ON s.Reorder_ID = si.Reorder_ID
    JOIN Product AS p ON si.UPC_Code = p.UPC_Code
    WHERE s.Warehouse_ID = """
        + warehouse_id
        + ";"
    )
    cursor.execute(query)
    reorders = cursor.fetchall()
    print("Warehouses: " + str(warehouse_id) + "'s reorder history")
    for reorder in reorders:
        print(
            " Reorder ID: "
            + str(reorder[0])
            + " Status: "
            + str(reorder[1])
            + " Vendor ID: "
            + str(reorder[3])
            + " Product: ("
            + str(reorder[7])
            + ") "
            + reorder[8]
            + " Quantity: "
            + str(reorder[4])
        )
    input("Enter to Contiune")


def WarehouseInventoryLevels():
    # warehouse login
    os.system("cls")
    warehouse_id = input("Input Warehouse ID: ")
    query = "SELECT * FROM Warehouse WHERE Warehouse_ID =" + warehouse_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        warehouse_id = input("Input Valid Warehouse ID: ")
        query = "SELECT * FROM Warehouse WHERE Warehouse_ID =" + warehouse_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")
    query = (
        "SELECT * FROM Warehouse_Inventory as i JOIN Product as p ON i.UPC_Code = p.UPC_Code where i.Warehouse_ID = "
        + warehouse_id
        + " ORDER BY i.Amount DESC"
    )
    cursor.execute(query)
    inventory = cursor.fetchall()
    print("Warehouses: " + str(warehouse_id) + "'s Inventory Level:")
    for item in inventory:
        print(
            "Product: ("
            + str(item[4])
            + ") "
            + item[5]
            + " Amount: "
            + str(item[0])
            + " Max Capacity: "
            + str(item[1])
        )
    input("Enter to Contiune")


def VendorMenu():
    os.system("cls")
    runMenu = True
    while runMenu:
        first_selection = input(
            """Select Interface:\n
        1. Fufill Reorders/Create Shipments\n
        2. View Shipment History\n
        3. Exit
        """
        )
        try:
            fselection = int(first_selection)
        except:
            input("Invalid input\n press enter to retry")
            try:
                os.system("cls")
            except:
                os.system("cls")
            continue
        if fselection < 1 or fselection > 3:
            input("Invalid input\n press enter to retry")
            continue
        match (fselection):
            case 1:
                shipment()
            case 2:
                ShipmentHistory()
            case 3:
                print("Exiting")
                runMenu = False
                os.system("cls")
                break
            case _:
                input("Invalid input\n press enter to retry")
                continue


def ShipmentHistory():
    # Vendor login
    os.system("cls")
    vendor_id = input("Input Vendor ID: ")
    query = "SELECT * FROM Vendor WHERE Vendor_ID =" + vendor_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        vendor_id = input("Input Valid Vendor ID: ")
        query = "SELECT * FROM Vendor WHERE Vendor_ID =" + vendor_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")
    query = (
        """
    SELECT *
        FROM Shipment AS s
        JOIN Shipment_Item AS si ON s.Shipment_ID = si.Shipment_ID
        JOIN Product AS p ON si.UPC_Code = p.UPC_Code
        WHERE s.Vendor_ID = """
        + vendor_id
        + " ORDER BY s.Shipment_Date DESC, s.Time_Hour DESC, s.Time_Minute DESC;"
    )
    cursor.execute(query)
    shipments = cursor.fetchall()
    print("Vendor: " + str(vendor_id) + "'s shipment history")
    for shipment in shipments:
        formatted_date = shipment[1].strftime("%B %d, %Y")
        print(
            formatted_date
            + " "
            + str(shipment[2])
            + ":"
            + str(shipment[3])
            + " Shipment ID: "
            + str(shipment[0])
            + " Status: "
            + str(getShipmentStats(shipment[4]))
            + " Warehouse ID: "
            + str(shipment[5])
            + " Product: ("
            + str(shipment[10])
            + ") "
            + shipment[11]
            + " Quantity: "
            + str(shipment[7])
        )
    input("Enter to Contiune")


def getShipmentStats(intStatus):
    if intStatus == 0:
        return "Completed"
    else:
        return "Shipped"


def MarketMenu():
    os.system("cls")
    runMenu = True
    while runMenu:
        first_selection = input(
            """Select Interface:\n
        1. Run OLAP Queries\n
        2. Exit
        """
        )
        try:
            fselection = int(first_selection)
        except:
            input("Invalid input\n press enter to retry")
            try:
                os.system("cls")
            except:
                os.system("cls")
            continue
        if fselection < 1 or fselection > 2:
            input("Invalid input\n press enter to retry")
            continue
        match (fselection):
            case 1:
                OLAP()
            case 2:
                print("Exiting")
                runMenu = False
                os.system("cls")
                break
            case _:
                input("Invalid input\n press enter to retry")
                continue


def runMainMenu():
    os.system("cls")
    runMenu = True
    while runMenu:
        first_selection = input(
            """Select User:
        1. Customer\n
        2. Store\n
        3. Warehouse\n
        4. Vendor\n
        5. Market-Researcher\n
        6. Store Register\n
        7. Exit
        """
        )
        try:
            fselection = int(first_selection)
        except:
            input("Invalid input\n press enter to retry")
            try:
                os.system("cls")
            except:
                os.system("cls")
            continue
        if fselection < 1 or fselection > 7:
            input("Invalid input\n press enter to retry")
            continue
        match (fselection):
            case 1:
                customerMenu()
            case 2:
                StoreMenu()
            case 3:
                WarehouseMenu()
            case 4:
                VendorMenu()
            case 5:
                MarketMenu()
            case 6:
                checkout()
            case 7:
                print("Exiting")
                runMenu = False
                os.system("cls")
                return -1
            case _:
                input("Invalid input\n press enter to retry")
                continue


# OLAP


def OLAP():
    os.system("cls")

    rselection = input(
        """Select overview:
            1. Inventory Value\n
            2. Total Product by Vendor\n
            3. Average Inventory Levels\n
            4. Top Customers\n
            5. Best Sellers by Store\n
            6. Best Sellers by Region\n
            7. Top 3 Stores by Sales\n
            8. How many stores Pistols outsell Rifles\n
            9. Top Product people buy in addition to tents\n
            """
    )
    try:
        selection = int(rselection)
    except:
        input("Invalid input\n press enter to retry")
        OLAP()

    if selection < 1 or selection > 9:
        input("Invalid input\n press enter to retry")
        OLAP()
    os.system("cls")
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
                        print(
                            "Total enteprise inventory value: "
                            + str(row[2])
                            .strip("(")
                            .strip(")")
                            .strip(",")
                            .strip("Decimal")
                            + "\n"
                        )
                    elif row[1] == None:
                        print(
                            "Total inventory value in Region "
                            + getRegion(row[0])
                            + ": "
                            + str(row[2])
                            .strip("(")
                            .strip(")")
                            .strip(",")
                            .strip("Decimal")
                        )
                    else:
                        print(
                            "Inventory value in Store "
                            + str(row[1])
                            + ": "
                            + str(row[2])
                            .strip("(")
                            .strip(")")
                            .strip(",")
                            .strip("Decimal")
                        )
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
                    elif row[1] == None:
                        print(
                            "Total unique products in Region "
                            + str(row[0])
                            + ": "
                            + str(row[2])
                        )
                    else:
                        print(
                            "Total unique products from Vendor "
                            + str(row[1])
                            + " in Region "
                            + str(row[0])
                            + ": "
                            + str(row[2])
                        )
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
                        print(
                            "Average enterprise warehouse stock: "
                            + str(row[2]).strip("Decimal")
                        )
                    elif row[1] == None:
                        print(
                            "Average warehouse stock in Region "
                            + str(row[0])
                            + ": "
                            + str(row[2]).strip("Decimal")
                        )
                    else:
                        print(
                            "Average warehouse stock of "
                            + str(row[1])
                            + " in Region "
                            + str(row[0])
                            + ": "
                            + str(row[2]).strip("Decimal")
                        )

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
                    print(
                        str(row[4])
                        + ". "
                        + str(row[1])
                        + " "
                        + str(row[2])
                        + " (ID: "
                        + str(row[0])
                        + ") Total purchase amount : "
                        + str(row[3]).strip("Decimal")
                    )
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
                        space = ""

                    print(
                        space
                        + str(row[4])
                        + ". "
                        + row[1]
                        + " (ID: "
                        + str(row[2])
                        + ") "
                        + "Quantity Sold: "
                        + str(row[3]).strip("Decimal")
                    )
            except mysql.connector.Error as error:
                print(error)
                input("\npress enter to continue\n")
        case 6:
            # best sellers by region
            query = """ WITH Sales AS (
    SELECT s.Region, p.Name, p.UPC_Code, SUM(si.Quanity) as Total_Sales,
        ROW_NUMBER() OVER (PARTITION BY s.Region ORDER BY SUM(si.Quanity) DESC) as Sales_Rank
    FROM Store s
    JOIN Sale sa ON s.Store_ID = sa.Store_ID
    JOIN Sale_Item si ON sa.Sale_ID = si.Sale_ID
    JOIN Product p ON si.UPC_Code = p.UPC_Code
    GROUP BY s.Region, p.Name, p.UPC_Code
)
SELECT * FROM Sales WHERE Sales_Rank <= 5;
"""
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                print("Best Sellers by Region:")
                store = ""
                for row in results:
                    if str(row[0]) != store:
                        store = str(row[0])
                        space = "\n Region " + store + ": \n"
                    else:
                        space = ""

                    print(
                        space
                        + str(row[4])
                        + ". "
                        + row[1]
                        + " (ID: "
                        + str(row[2])
                        + ") "
                        + "Quantity Sold: "
                        + str(row[3]).strip("Decimal")
                    )
            except mysql.connector.Error as error:
                print(error)
                input("\npress enter to continue\n")
        case 7:
            query = """
            WITH StoreSales AS (
                SELECT s.Store_ID, SUM(si.Local_Price * si.Quanity) AS Total_Sales
                FROM Store s
                JOIN Sale sa ON s.Store_ID = sa.Store_ID
                JOIN Sale_Item si ON sa.Sale_ID = si.Sale_ID
                GROUP BY s.Store_ID
                    ),
            RankedStoreSales AS (
                SELECT Store_ID, Total_Sales,
                ROW_NUMBER() OVER (ORDER BY Total_Sales DESC) AS Sales_Rank
                FROM StoreSales
            )
            SELECT Store_ID, Total_Sales
            FROM RankedStoreSales
            WHERE Sales_Rank <= 3;
"""
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                print("Top 3 Stores by Sales")
                for result in results:
                    print(
                        "Store: " + str(result[0]) + " Sales: $" + str(int(result[1]))
                    )
            except mysql.connector.Error as error:
                print(error)
                input("\npress enter to continue\n")
        case 8:
            query = """
WITH PistolSales AS (
    SELECT s.Store_ID, SUM(si.Quanity) AS Total_Pistol_Sales
    FROM Store s
    JOIN Sale sa ON s.Store_ID = sa.Store_ID
    JOIN Sale_Item si ON sa.Sale_ID = si.Sale_ID
    JOIN Product p ON si.UPC_Code = p.UPC_Code
    WHERE EXISTS (SELECT 1 FROM Pistol pt WHERE pt.UPC_Code = p.UPC_Code)
    GROUP BY s.Store_ID
),
RifleSales AS (
    SELECT s.Store_ID, SUM(si.Quanity) AS Total_Rifle_Sales
    FROM Store s
    JOIN Sale sa ON s.Store_ID = sa.Store_ID
    JOIN Sale_Item si ON sa.Sale_ID = si.Sale_ID
    JOIN Product p ON si.UPC_Code = p.UPC_Code
    WHERE EXISTS (SELECT 1 FROM Rifle rf WHERE rf.UPC_Code = p.UPC_Code)
    GROUP BY s.Store_ID
),
StoreSalesComparison AS (
    SELECT p.Store_ID, p.Total_Pistol_Sales, r.Total_Rifle_Sales
    FROM PistolSales p
    JOIN RifleSales r ON p.Store_ID = r.Store_ID
    WHERE p.Total_Pistol_Sales > r.Total_Rifle_Sales
)
SELECT Store_ID, Total_Pistol_Sales, Total_Rifle_Sales
FROM StoreSalesComparison;
            """
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                print("Pistols outsell Rifles in: " + str(len(results)) + " stores")
                for result in results:
                    print(
                        "Store: "
                        + str(result[0])
                        + " Pistol Sales: "
                        + str(int(result[1]))
                        + " Rifles Sales: "
                        + str(int(result[2]))
                    )
            except mysql.connector.Error as error:
                print(error)
                input("\npress enter to continue\n")
        case 9:
            query = """
            WITH TentSales AS (
                SELECT sa.Sale_ID
                FROM Sale sa
                JOIN Sale_Item si ON sa.Sale_ID = si.Sale_ID
                JOIN Product p ON si.UPC_Code = p.UPC_Code
                WHERE p.Name = 'Tent'
                ),
            CoSales AS (
                SELECT si2.UPC_Code, p2.Name, COUNT(*) AS Total_Sales
                FROM TentSales ts
                JOIN Sale_Item si2 ON ts.Sale_ID = si2.Sale_ID
                JOIN Product p2 ON si2.UPC_Code = p2.UPC_Code
                WHERE p2.Name != 'Tent'
                GROUP BY si2.UPC_Code, p2.Name
                    )
            SELECT UPC_Code, Name, Total_Sales
            FROM CoSales
            ORDER BY Total_Sales DESC
            LIMIT 1;
            """
            cursor.execute(query)
            results = cursor.fetchall()
            print("Top item in addition of tents")
            for result in results:
                print("(" + str(result[0]) + ") " + result[1])

    rselection = input("")
    os.system("cls")


def webOrderMenu(avalibleProducts):
    os.system("cls")
    runMenu = True
    while runMenu:
        first_selection = input(
            """Select Product Type:
        1. Food\n
        2. Clothing\n
        3. Outdoor Gear\n
        4. All\n
        5. Exit
        """
        )
        try:
            fselection = int(first_selection)
        except:
            input("Invalid input\n press enter to retry")
            try:
                os.system("cls")
            except:
                os.system("cls")
            continue
        if fselection < 1 or fselection > 5:
            input("Invalid input\n press enter to retry")
            continue
        match (fselection):
            case 1:
                return FoodOrderMenu(avalibleProducts, 0)
            case 2:
                return ClothingOrderMenu(avalibleProducts, 0)
            case 3:
                return OutdoorGearOrderMenu(avalibleProducts, 0)
            case 4:
                return allOrderMenu(avalibleProducts, 0)
            case 5:
                print("Exiting")
                runMenu = False
                os.system("cls")
                break
            case _:
                input("Invalid input\n press enter to retry")
                continue


def allOrderMenu(avalibleProducts, currentIndex):
    allProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        outdoors = cursor.fetchall()
        if len(outdoors) != 0:
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price, p.UPC_Code, p.Brand_Name, p.Weight
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(outdoors[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allProducts.append(avaliable_products[0])
    if len(allProducts) == 0:
        print("No Products For Sale")
        input("Hit Enter to Contiune")
        return -1
    else:
        for products in allProducts:
            query = "SELECT * FROM Food WHERE UPC_Code =" + str(products[2]) + ";"
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                FoodOrderMenu([products], index)
                index += 1
                continue
            query = "SELECT * FROM Clothing WHERE UPC_Code =" + str(products[2]) + ";"
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                ClothingOrderMenu([products], index)
                index += 1
                continue
            query = (
                "SELECT * FROM Outdoor_Gear WHERE UPC_Code =" + str(products[2]) + ";"
            )
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                allOutdoorGearHuntingMenu([products], index)
                index += 1
                continue
            print(
                str(index)
                + ": "
                + products[0]
                + "\n\tAmount Avalible: "
                + str(int(products[1]))
                + "\n\tPrice: $"
                + str(products[3])
                + "\n\tBrand: "
                + str(products[5])
                + "\n\tWeight: "
                + str(products[6])
            )
            index += 1
        return allProducts


def FoodOrderMenu(avalibleProducts, currentIndex):
    allFoodProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, f.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Food AS f ON p.UPC_Code = f.UPC_Code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        foods = cursor.fetchall()
        if len(foods) != 0:
            formatted_date = foods[0][10].strftime("%B %d, %Y")
            print(
                str(index)
                + ": "
                + foods[0][1]
                + "\n\tAmount Avalible: "
                + str(int(foods[0][13]))
                + "\n\tPrice: $"
                + str(foods[0][2])
                + "\n\tBrand: "
                + foods[0][8]
                + "\n\tCalories: "
                + str(foods[0][11])
                + "\n\tExpiration Date: "
                + formatted_date
                + "\n"
            )
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(foods[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allFoodProducts.append(avaliable_products[0])
    if len(allFoodProducts) == 0:
        print("No Food Products Avalible")
        input("Press Enter to try Again")
        return -1
    return allFoodProducts


def ClothingOrderMenu(avalibleProducts, currentIndex):
    allClothingProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, c.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Clothing AS c ON p.UPC_Code = c.UPC_Code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        clothes = cursor.fetchall()
        if len(clothes) != 0:
            print(
                str(index)
                + ": "
                + clothes[0][1]
                + "\n\tAmount Avalible: "
                + str(int(clothes[0][13]))
                + "\n\tPrice: $"
                + str(clothes[0][2])
                + "\n\tBrand: "
                + clothes[0][8]
                + "\n\tSize: "
                + clothes[0][10]
                + "\n\tColor: "
                + clothes[0][11]
            )
            index += 1
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(clothes[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allClothingProducts.append(avaliable_products[0])
    if len(allClothingProducts) == 0:
        print("No Food Products Avalible")
        input("Press Enter to try Again")
        return -1
    return allClothingProducts


def OutdoorGearOrderMenu(avalibleProducts, currentIndex):
    os.system("cls")
    runMenu = True
    while runMenu:
        first_selection = input(
            """Select Outdoor Gear Product Type:
        1. Hunting Equipment\n
        2. Fishing Equipment\n
        3. Camping Equipment\n
        4. All\n
        5. Exit
        """
        )
        try:
            fselection = int(first_selection)
        except:
            input("Invalid input\n press enter to retry")
            try:
                os.system("cls")
            except:
                os.system("cls")
            continue
        if fselection < 1 or fselection > 5:
            input("Invalid input\n press enter to retry")
            continue
        match (fselection):
            case 1:
                return HuntingEquipmentOrderMenu(avalibleProducts, currentIndex)
            case 2:
                return FishingEquipmentOrderMenu(avalibleProducts, currentIndex)
            case 3:
                return CampingEquipmentOrderMenu(avalibleProducts, currentIndex)
            case 4:
                return allOutdoorGearHuntingMenu(avalibleProducts, currentIndex)
                print("All Outdoor Products")
            case 5:
                print("Exiting")
                runMenu = False
                os.system("cls")
                return -1
            case _:
                input("Invalid input\n press enter to retry")
                continue


def allOutdoorGearHuntingMenu(avalibleProducts, currentIndex):
    allOutdoorGearProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Outdoor_Gear AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        outdoors = cursor.fetchall()
        if len(outdoors) != 0:
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price, p.UPC_Code, p.Brand_Name, p.Weight
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(outdoors[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allOutdoorGearProducts.append(avaliable_products[0])
    if len(allOutdoorGearProducts) == 0:
        print("No Outdoor Gear Products")
        input("Hit Enter to Contiune")
        return -1
    else:
        for outs in allOutdoorGearProducts:
            query = (
                "SELECT * FROM Hunting_Equipment WHERE UPC_Code =" + str(outs[2]) + ";"
            )
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                allHuntingEquipmentOrderMenu([outs], index)
                index += 1
                continue
            query = (
                "SELECT * FROM Fishing_Equipment WHERE UPC_Code =" + str(outs[2]) + ";"
            )
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                allFishingOrderMenu([outs], index)
                index += 1
                continue
            query = (
                "SELECT * FROM Camping_Equipment WHERE UPC_Code =" + str(outs[2]) + ";"
            )
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                allCampingOrderMenu([outs], index)
                index += 1
                continue
            print(
                str(index)
                + ": "
                + outs[0]
                + "\n\tAmount Avalible: "
                + str(int(outs[1]))
                + "\n\tPrice: $"
                + str(outs[3])
                + "\n\tBrand: "
                + str(outs[5])
                + "\n\tWeight: "
                + str(outs[6])
            )
            index += 1
        return allOutdoorGearProducts


def HuntingEquipmentOrderMenu(avalibleProducts, currentIndex):
    os.system("cls")
    runMenu = True
    while runMenu:
        first_selection = input(
            """Select Hunting Equipment Product Type:
        1. Firearm\n
        2. Archery\n
        3. All\n
        4. Exit
        """
        )
        try:
            fselection = int(first_selection)
        except:
            input("Invalid input\n press enter to retry")
            try:
                os.system("cls")
            except:
                os.system("cls")
            continue
        if fselection < 1 or fselection > 4:
            input("Invalid input\n press enter to retry")
            continue
        match (fselection):
            case 1:
                return FirearmOrderMenu(avalibleProducts, currentIndex)
            case 2:
                return ArcheryOrderMenu(avalibleProducts, currentIndex)
            case 3:
                return allHuntingEquipmentOrderMenu(avalibleProducts, currentIndex)
            case 4:
                print("Exiting")
                runMenu = False
                os.system("cls")
                return -1
            case _:
                input("Invalid input\n press enter to retry")
                continue


def allHuntingEquipmentOrderMenu(avalibleProducts, currentIndex):
    allHuntingProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Hunting_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        huntings = cursor.fetchall()
        if len(huntings) != 0:
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price, p.UPC_Code, p.Brand_Name, p.Weight
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(huntings[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allHuntingProducts.append(avaliable_products[0])
    if len(allHuntingProducts) == 0:
        print("No Hunting Products")
        input("Hit Enter to Contiune")
        return -1
    else:
        for hunt in allHuntingProducts:
            query = "SELECT * FROM Firearm WHERE UPC_Code =" + str(hunt[2]) + ";"
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                allFireArmOrderMenu([hunt], index)
                index += 1
                continue
            query = "SELECT * FROM Archery WHERE UPC_Code =" + str(hunt[2]) + ";"
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                AllArcheryOrderMenu([hunt], index)
                index += 1
                continue
            print(
                str(index)
                + ": "
                + hunt[0]
                + "\n\tAmount Avalible: "
                + str(int(hunt[1]))
                + "\n\tPrice: $"
                + str(hunt[3])
                + "\n\tBrand: "
                + str(hunt[5])
                + "\n\tWeight: "
                + str(hunt[6])
            )
            index += 1
        return allHuntingProducts


def FirearmOrderMenu(avalibleProducts, currentIndex):
    os.system("cls")
    runMenu = True
    while runMenu:
        first_selection = input(
            """Select Firearm Product Type:
        1. Rifle\n
        2. Shotgun\n
        3. Pistol\n
        4. All\n
        5. Exit
        """
        )
        try:
            fselection = int(first_selection)
        except:
            input("Invalid input\n press enter to retry")
            try:
                os.system("cls")
            except:
                os.system("cls")
            continue
        if fselection < 1 or fselection > 5:
            input("Invalid input\n press enter to retry")
            continue
        match (fselection):
            case 1:
                return RifleOrderMenu(avalibleProducts, currentIndex)
            case 2:
                return ShotgunOrderMenu(avalibleProducts, currentIndex)
            case 3:
                return PistolOrderMenu(avalibleProducts, currentIndex)
            case 4:
                return allFireArmOrderMenu(avalibleProducts, currentIndex)
            case 5:
                print("Exiting")
                runMenu = False
                os.system("cls")
                return -1
            case _:
                input("Invalid input\n press enter to retry")
                continue


def allFireArmOrderMenu(avalibleProducts, currentIndex):
    allFirearmProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, f.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Firearm AS f on p.UPC_Code = f.UPC_Code
                    JOIN Hunting_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        firearms = cursor.fetchall()
        if len(firearms) != 0:
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price, p.UPC_Code, p.Brand_Name, p.Weight
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(firearms[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allFirearmProducts.append(avaliable_products[0])
    if len(allFirearmProducts) == 0:
        print("No Firearm Products")
        input("Hit Enter to Contiune")
        return -1
    else:
        for firearm in allFirearmProducts:
            query = "SELECT * FROM Rifle WHERE UPC_Code =" + str(firearm[2]) + ";"
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                RifleOrderMenu([firearm], index)
                index += 1
                continue
            query = "SELECT * FROM Shotgun WHERE UPC_Code =" + str(firearm[2]) + ";"
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                ShotgunOrderMenu([firearm], index)
                index += 1
                continue
            query = "SELECT * FROM Pistol WHERE UPC_Code =" + str(firearm[2]) + ";"
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                PistolOrderMenu([firearm], index)
                index += 1
                continue
            print(
                str(index)
                + ": "
                + firearm[0]
                + "\n\tAmount Avalible: "
                + str(int(firearm[1]))
                + "\n\tPrice: $"
                + str(firearm[3])
                + "\n\tBrand: "
                + str(firearm[5])
                + "\n\tWeight: "
                + str(firearm[6])
            )
            index += 1
        return allFirearmProducts


def RifleOrderMenu(avalibleProducts, currentIndex):
    allRifleProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, f.*, r.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Rifle AS r ON p.UPC_Code = r.UPC_Code
                    JOIN Firearm AS f on p.UPC_Code = f.UPC_Code
                    JOIN Hunting_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        rifles = cursor.fetchall()
        if len(rifles) != 0:
            print(
                str(index)
                + ": "
                + rifles[0][1]
                + "\n\tAmount Avalible: "
                + str(int(rifles[0][20]))
                + "\n\tPrice: $"
                + str(rifles[0][2])
                + "\n\tBrand: "
                + rifles[0][8]
                + "\n\tHunting Type: "
                + rifles[0][10]
                + "\n\tColor: "
                + rifles[0][13]
                + "\n\tCapacity: "
                + str(rifles[0][12])
                + "\n\tCaliber: "
                + rifles[0][16]
                + "\n\tAction Type: "
                + rifles[0][18]
                + "\n\tBarrel Length: "
                + str(rifles[0][14])
                + "\n\tStock Length: "
                + rifles[0][17]
            )
            index += 1
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(rifles[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allRifleProducts.append(avaliable_products[0])
    if len(allRifleProducts) == 0:
        print("No Rifle Products Avalible")
        input("Press Enter to try Again")
        return -1
    return allRifleProducts


def ShotgunOrderMenu(avalibleProducts, currentIndex):
    allShotgunProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, f.*, s.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Shotgun AS s ON p.UPC_Code = s.UPC_Code
                    JOIN Firearm AS f on p.UPC_Code = f.UPC_Code
                    JOIN Hunting_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        shotguns = cursor.fetchall()
        if len(shotguns) != 0:
            print(
                str(index)
                + ": "
                + shotguns[0][1]
                + "\n\tAmount Avalible: "
                + str(int(shotguns[0][19]))
                + "\n\tPrice: $"
                + str(shotguns[0][2])
                + "\n\tBrand: "
                + shotguns[0][8]
                + "\n\tHunting Type: "
                + shotguns[0][10]
                + "\n\tColor: "
                + shotguns[0][13]
                + "\n\tCapacity: "
                + str(shotguns[0][12])
                + "\n\tGauge: "
                + shotguns[0][16]
                + "\n\tBarrel Length: "
                + str(shotguns[0][14])
                + "\n\tChoke: "
                + shotguns[0][17]
            )
            index += 1
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(shotguns[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allShotgunProducts.append(avaliable_products[0])
    if len(allShotgunProducts) == 0:
        print("No Shotguns Products Avalible")
        input("Press Enter to try Again")
        return -1
    return allShotgunProducts


def PistolOrderMenu(avalibleProducts, currentIndex):
    allPistolProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, f.*, s.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Pistol AS s ON p.UPC_Code = s.UPC_Code
                    JOIN Firearm AS f on p.UPC_Code = f.UPC_Code
                    JOIN Hunting_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        pistols = cursor.fetchall()
        if len(pistols) != 0:
            print(
                str(index)
                + ": "
                + pistols[0][1]
                + "\n\tAmount Avalible: "
                + str(int(pistols[0][19]))
                + "\n\tPrice: $"
                + str(pistols[0][2])
                + "\n\tBrand: "
                + pistols[0][8]
                + "\n\tHunting Type: "
                + pistols[0][10]
                + "\n\tColor: "
                + pistols[0][13]
                + "\n\tCapacity: "
                + str(pistols[0][12])
                + "\n\tCaliber: "
                + pistols[0][16]
                + "\n\tBarrel Length: "
                + str(pistols[0][14])
                + "\n\tConcealable: "
                + pistols[0][17]
            )
            index += 1
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(pistols[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allPistolProducts.append(avaliable_products[0])
    if len(allPistolProducts) == 0:
        print("No Pistol Products Avalible")
        input("Press Enter to try Again")
        return -1
    return allPistolProducts


def ArcheryOrderMenu(avalibleProducts, currentIndex):
    os.system("cls")
    runMenu = True
    while runMenu:
        first_selection = input(
            """Select Archery Product Type:
        1. Bow\n
        2. Arrow\n
        3. All\n
        4. Exit
        """
        )
        try:
            fselection = int(first_selection)
        except:
            input("Invalid input\n press enter to retry")
            try:
                os.system("cls")
            except:
                os.system("cls")
            continue
        if fselection < 1 or fselection > 4:
            input("Invalid input\n press enter to retry")
            continue
        match (fselection):
            case 1:
                return BowOrderMenu(avalibleProducts, currentIndex)
            case 2:
                return ArrowOrderMenu(avalibleProducts, currentIndex)
            case 3:
                return AllArcheryOrderMenu(avalibleProducts, currentIndex)
            case 4:
                print("Exiting")
                runMenu = False
                os.system("cls")
                return -1
            case _:
                input("Invalid input\n press enter to retry")
                continue


def AllArcheryOrderMenu(avalibleProducts, currentIndex):
    print("Menu")
    allArcheryProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, f.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Archery AS f on p.UPC_Code = f.UPC_Code
                    JOIN Hunting_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        archerys = cursor.fetchall()
        if len(archerys) != 0:
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price, p.UPC_Code, p.Brand_Name, p.Weight
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(archerys[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allArcheryProducts.append(avaliable_products[0])
    if len(allArcheryProducts) == 0:
        print("No Archery Products")
        input("Hit Enter to Contiune")
        return -1
    else:
        for archery in allArcheryProducts:
            query = "SELECT * FROM Bows WHERE UPC_Code =" + str(archery[2]) + ";"
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                BowOrderMenu([archery], index)
                index += 1
                continue
            query = "SELECT * FROM Arrows WHERE UPC_Code =" + str(archery[2]) + ";"
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                ArrowOrderMenu([archery], index)
                index += 1
                continue
            print(
                str(index)
                + ": "
                + archery[0]
                + "\n\tAmount Avalible: "
                + str(int(archery[1]))
                + "\n\tPrice: $"
                + str(archery[3])
                + "\n\tBrand: "
                + str(archery[5])
                + "\n\tWeight: "
                + str(archery[6])
            )
            index += 1
        return allArcheryProducts


def BowOrderMenu(avalibleProducts, currentIndex):
    print("All Bows")
    allBowsProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, f.*, s.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Bows AS s ON p.UPC_Code = s.UPC_Code
                    JOIN Archery AS f on p.UPC_Code = f.UPC_Code
                    JOIN Hunting_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        bows = cursor.fetchall()
        if len(bows) != 0:
            print(
                str(index)
                + ": "
                + bows[0][1]
                + "\n\tAmount Avalible: "
                + str(int(bows[0][20]))
                + "\n\tPrice: $"
                + str(bows[0][2])
                + "\n\tBrand: "
                + bows[0][8]
                + "\n\tHunting Type: "
                + bows[0][10]
                + "\n\tArchery Type: "
                + str(bows[0][12])
                + "\n\Bow Type: "
                + bows[0][14]
                + "\n\Draw Weight: "
                + str(bows[0][15])
                + "\n\Let Off: "
                + str(bows[0][16])
            )
            index += 1
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(bows[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allBowsProducts.append(avaliable_products[0])
    if len(allBowsProducts) == 0:
        print("No Bow Products Avalible")
        input("Press Enter to try Again")
        return -1
    return allBowsProducts


def ArrowOrderMenu(avalibleProducts, currentIndex):
    allArrowProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, f.*, s.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Arrows AS s ON p.UPC_Code = s.UPC_Code
                    JOIN Archery AS f on p.UPC_Code = f.UPC_Code
                    JOIN Hunting_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        arrows = cursor.fetchall()
        if len(arrows) != 0:
            print(
                str(index)
                + ": "
                + arrows[0][1]
                + "\n\tAmount Avalible: "
                + str(int(arrows[0][18]))
                + "\n\tPrice: $"
                + str(arrows[0][2])
                + "\n\tBrand: "
                + arrows[0][8]
                + "\n\tHunting Type: "
                + arrows[0][10]
                + "\n\tArchery Type: "
                + str(arrows[0][12])
                + "\n\Length: "
                + str(arrows[0][14])
                + "\n\Tip Grain: "
                + str(arrows[0][15])
                + "\n\Weight: "
                + str(arrows[0][16])
            )
            index += 1
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(arrows[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allArrowProducts.append(avaliable_products[0])
    if len(allArrowProducts) == 0:
        print("No Arrow Products Avalible")
        input("Press Enter to try Again")
        return -1
    return allArrowProducts


def FishingEquipmentOrderMenu(avalibleProducts, currentIndex):
    os.system("cls")
    runMenu = True
    while runMenu:
        first_selection = input(
            """Select Fishing Equipment Product Type:
        1. Rods\n
        2. Reels\n
        3. Bait and Lures\n
        4. All\n
        5. Exit
        """
        )
        try:
            fselection = int(first_selection)
        except:
            input("Invalid input\n press enter to retry")
            try:
                os.system("cls")
            except:
                os.system("cls")
            continue
        if fselection < 1 or fselection > 5:
            input("Invalid input\n press enter to retry")
            continue
        match (fselection):
            case 1:
                return RodsOrderMenu(avalibleProducts, currentIndex)
            case 2:
                return ReelsOrderMenu(avalibleProducts, currentIndex)
            case 3:
                return BaitAndLuresOrderMenu(avalibleProducts, currentIndex)
            case 4:
                return allFishingOrderMenu(avalibleProducts, currentIndex)
            case 5:
                print("Exiting")
                runMenu = False
                os.system("cls")
                break
            case _:
                input("Invalid input\n press enter to retry")
                continue


def allFishingOrderMenu(avalibleProducts, currentIndex):
    allFishingProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Fishing_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        fishings = cursor.fetchall()
        if len(fishings) != 0:
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price, p.UPC_Code, p.Brand_Name, p.Weight
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(fishings[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allFishingProducts.append(avaliable_products[0])
    if len(allFishingProducts) == 0:
        print("No Fishing Products")
        input("Hit Enter to Contiune")
        return -1
    else:
        for fishing in allFishingProducts:
            query = "SELECT * FROM Rods WHERE UPC_Code =" + str(fishing[2]) + ";"
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                RodsOrderMenu([fishing], index)
                index += 1
                continue
            query = "SELECT * FROM Reels WHERE UPC_Code =" + str(fishing[2]) + ";"
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                ReelsOrderMenu([fishing], index)
                index += 1
                continue
            query = (
                "SELECT * FROM Bait_and_Lures WHERE UPC_Code =" + str(fishing[2]) + ";"
            )
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                BaitAndLuresOrderMenu([fishing], index)
                index += 1
                continue
            print(
                str(index)
                + ": "
                + fishing[0]
                + "\n\tAmount Avalible: "
                + str(int(fishing[1]))
                + "\n\tPrice: $"
                + str(fishing[3])
                + "\n\tBrand: "
                + str(fishing[5])
                + "\n\tWeight: "
                + str(fishing[6])
            )
            index += 1
        return allFishingProducts


def RodsOrderMenu(avalibleProducts, currentIndex):
    allRodProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, s.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Rods AS s ON p.UPC_Code = s.UPC_Code
                    JOIN Fishing_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        rods = cursor.fetchall()
        if len(rods) != 0:
            print(
                str(index)
                + ": "
                + rods[0][1]
                + "\n\tAmount Avalible: "
                + str(int(rods[0][17]))
                + "\n\tPrice: $"
                + str(rods[0][2])
                + "\n\tBrand: "
                + rods[0][8]
                + "\n\tWater Type: "
                + rods[0][10]
                + "\n\tLength: "
                + str(rods[0][12])
                + "\n\tPower: "
                + str(rods[0][13])
                + "\n\tRod Type: "
                + str(rods[0][14])
                + "\n\tMaterial: "
                + str(rods[0][15])
            )
            index += 1
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(rods[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allRodProducts.append(avaliable_products[0])
    if len(allRodProducts) == 0:
        print("No Rods Avalible")
        input("Press Enter to try Again")
        return -1
    return allRodProducts


def ReelsOrderMenu(avalibleProducts, currentIndex):
    allReelProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, s.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Reels AS s ON p.UPC_Code = s.UPC_Code
                    JOIN Fishing_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        reels = cursor.fetchall()
        if len(reels) != 0:
            print(
                str(index)
                + ": "
                + reels[0][1]
                + "\n\tAmount Avalible: "
                + str(int(reels[0][16]))
                + "\n\tPrice: $"
                + str(reels[0][2])
                + "\n\tBrand: "
                + reels[0][8]
                + "\n\tWater Type: "
                + reels[0][10]
                + "\n\tGear Ration: "
                + str(reels[0][12])
                + "\n\tLine Capcity: "
                + str(reels[0][13])
                + "\n\tReel Type: "
                + str(reels[0][14])
            )
            index += 1
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(reels[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allReelProducts.append(avaliable_products[0])
    if len(allReelProducts) == 0:
        print("No Reels Avalible")
        input("Press Enter to try Again")
        return -1
    return allReelProducts


def BaitAndLuresOrderMenu(avalibleProducts, currentIndex):
    allBaitProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, s.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Bait_and_Lures AS s ON p.UPC_Code = s.UPC_Code
                    JOIN Fishing_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        baits = cursor.fetchall()
        if len(baits) != 0:
            print(
                str(index)
                + ": "
                + baits[0][1]
                + "\n\tAmount Avalible: "
                + str(int(baits[0][16]))
                + "\n\tPrice: $"
                + str(baits[0][2])
                + "\n\tBrand: "
                + baits[0][8]
                + "\n\tWater Type: "
                + baits[0][10]
                + "\n\tBait Type: "
                + str(baits[0][12])
                + "\n\tSize: "
                + str(baits[0][13])
                + "\n\tMaterial: "
                + str(baits[0][14])
            )
            index += 1
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(baits[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allBaitProducts.append(avaliable_products[0])
    if len(allBaitProducts) == 0:
        print("No Bait or Lures Avalible")
        input("Press Enter to try Again")
        return -1
    return allBaitProducts


def CampingEquipmentOrderMenu(avalibleProducts, currentIndex):
    os.system("cls")
    runMenu = True
    while runMenu:
        first_selection = input(
            """Select Camping Product Type:
        1. Tents\n
        2. Sleeping Bags\n
        3. All\n
        4. Exit
        """
        )
        try:
            fselection = int(first_selection)
        except:
            input("Invalid input\n press enter to retry")
            try:
                os.system("cls")
            except:
                os.system("cls")
            continue
        if fselection < 1 or fselection > 4:
            input("Invalid input\n press enter to retry")
            continue
        match (fselection):
            case 1:
                return TentsOrderMenu(avalibleProducts, currentIndex)
            case 2:
                return SleepingBagsOrderMenu(avalibleProducts, currentIndex)
            case 3:
                return allCampingOrderMenu(avalibleProducts, currentIndex)
                print("All Camping")
            case 4:
                print("Exiting")
                runMenu = False
                os.system("cls")
                break
            case _:
                input("Invalid input\n press enter to retry")
                continue


def allCampingOrderMenu(avalibleProducts, currentIndex):
    allCampingProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Camping_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        campings = cursor.fetchall()
        if len(campings) != 0:
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price, p.UPC_Code, p.Brand_Name, p.Weight
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(campings[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allCampingProducts.append(avaliable_products[0])
    if len(allCampingProducts) == 0:
        print("No Camping Products")
        input("Hit Enter to Contiune")
        return -1
    else:
        for camping in allCampingProducts:
            query = "SELECT * FROM Tents WHERE UPC_Code =" + str(camping[2]) + ";"
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                TentsOrderMenu([camping], index)
                index += 1
                continue
            query = (
                "SELECT * FROM Sleeping_Bags WHERE UPC_Code =" + str(camping[2]) + ";"
            )
            cursor.execute(query)
            if len(cursor.fetchall()) != 0:
                SleepingBagsOrderMenu([camping], index)
                index += 1
                continue
            print(
                str(index)
                + ": "
                + camping[0]
                + "\n\tAmount Avalible: "
                + str(int(camping[1]))
                + "\n\tPrice: $"
                + str(camping[3])
                + "\n\tBrand: "
                + str(camping[5])
                + "\n\tWeight: "
                + str(camping[6])
            )
            index += 1
        return allCampingProducts


def TentsOrderMenu(avalibleProducts, currentIndex):
    allTentProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, s.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Tents AS s ON p.UPC_Code = s.UPC_Code
                    JOIN Camping_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        tents = cursor.fetchall()
        if len(tents) != 0:
            print(
                str(index)
                + ": "
                + tents[0][1]
                + "\n\tAmount Avalible: "
                + str(int(tents[0][16]))
                + "\n\tPrice: $"
                + str(tents[0][2])
                + "\n\tBrand: "
                + tents[0][8]
                + "\n\tCold Rating: "
                + tents[0][10]
                + "\n\tCapacity: "
                + str(tents[0][12])
                + "\n\tSetup Time:"
                + str(tents[0][13])
                + "\n\tMaterial: "
                + str(tents[0][14])
            )
            index += 1
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(tents[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allTentProducts.append(avaliable_products[0])
    if len(allTentProducts) == 0:
        print("No Tents Avalible")
        input("Press Enter to try Again")
        return -1
    return allTentProducts


def SleepingBagsOrderMenu(avalibleProducts, currentIndex):
    allSleepingBagProducts = []
    index = currentIndex
    for product in avalibleProducts:
        query = (
            """SELECT p.*, h.*, s.*, SUM(i.Amount) AS Total_Amount
                    FROM Product AS p
                    JOIN Sleeping_Bags AS s ON p.UPC_Code = s.UPC_Code
                    JOIN Camping_Equipment AS h on p.UPC_Code = h.UPC_code
                    JOIN Inventory AS i ON p.UPC_Code = i.UPC_Code
                    WHERE p.UPC_Code = """
            + str(product[4])
            + " GROUP BY p.UPC_Code;"
        )
        cursor.execute(query)
        bags = cursor.fetchall()
        if len(bags) != 0:
            print(
                str(index)
                + ": "
                + bags[0][1]
                + "\n\tAmount Avalible: "
                + str(int(bags[0][16]))
                + "\n\tPrice: $"
                + str(bags[0][2])
                + "\n\tBrand: "
                + bags[0][8]
                + "\n\tCold Rating: "
                + bags[0][10]
                + "\n\tCapacity: "
                + str(bags[0][12])
                + "\n\tInsulation Type:"
                + str(bags[0][13])
                + "\n\tMoisture Wicking: "
                + str(bags[0][14])
            )
            index += 1
            query = (
                """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price
        FROM Inventory i
        JOIN Product p ON i.UPC_Code = p.UPC_Code
        JOIN Store st ON i.Store_ID = st.Store_ID
        WHERE i.Amount > 0 AND  p.UPC_Code ="""
                + str(bags[0][0])
                + " GROUP BY p.Name, p.UPC_Code, p.Price;"
            )
            cursor.execute(query)
            avaliable_products = cursor.fetchall()
            allSleepingBagProducts.append(avaliable_products[0])
    if len(allSleepingBagProducts) == 0:
        print("No Sleeping Bags Avalible")
        input("Press Enter to try Again")
        return -1
    return allSleepingBagProducts


# web orders


def webOrder():
    os.system("cls")
    validLogin = False
    while not validLogin:
        login = input("input ur id to login or -1 to register: \n")
        if login == str(-1):
            login = register()
            validLogin = True
            break
        # check if customer exists in database
        query = "SELECT * FROM Customer WHERE Customer_ID = " + login
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")
        if not cursor.fetchone():
            # no id
            input("Not a Valid ID, press enter to try again")
            continue
        validLogin = True
        break
    # get  info for instock products (accross all stores)
    query = """
        SELECT DISTINCT p.name, SUM(i.Amount), p.UPC_Code, p.Price, p.UPC_Code
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
    while (not validSelection) or (not validAmount):
        index = 0
        product_selection = input(
            "Enter the number corresponding to the product you want to purchase: \n"
        )
        try:
            if (
                int(product_selection) > len(avaliable_products) - 1
                or int(product_selection) < 0
            ):
                input("Not a valid product please press enter to try again")
                continue
            else:
                validSelection = True
        except:
            input("Not a valid product please press enter to try again")
            continue
        amount = input("Enter the amount you want to purchaes: \n")
        try:
            intAmount = int(amount)
            if intAmount > float(avaliable_products[int(product_selection)][1]):
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

    # get store info for each store where product is in stock
    query = (
        "SELECT st.Store_ID, st.Region, p.Name, i.Amount, p.UPC_Code, p.Price FROM Inventory i JOIN Product p ON i.UPC_Code = p.UPC_Code JOIN Store st ON i.Store_ID = st.Store_ID WHERE p.UPC_Code ="
        + str(avaliable_products[int(product_selection)][2])
    )
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
        while intAmount > 0:
            for store in allStoresInner:
                if float(store[3]) <= 0 or store[0] in usedStoreIDs:
                    continue
                if inRegion:
                    if customerRegion[0][0] == str(store[1]):
                        if intAmount >= float(store[3]):
                            # update inventory of the item purchased for the store it was purchased from
                            query = (
                                "UPDATE Inventory SET Amount = Amount -"
                                + str(store[3])
                                + " WHERE store_id = "
                                + str(store[0])
                                + " AND UPC_Code = "
                                + str(store[4])
                                + ";"
                            )
                            cursor.execute(query)
                            # add to purchase to purchases array
                            purchases.append(
                                [
                                    str(store[0]),
                                    str(store[4]),
                                    str(store[3]),
                                    str(store[5]),
                                    str(store[2]),
                                ]
                            )
                            intAmount -= int(store[3])
                            usedStoreIDs.append(int(store[0]))
                            if intAmount <= 0:
                                break

                        else:
                            query = (
                                "UPDATE Inventory SET Amount = Amount -"
                                + str(intAmount)
                                + " WHERE store_id = "
                                + str(store[0])
                                + " AND UPC_Code = "
                                + str(store[4])
                                + ";"
                            )
                            cursor.execute(query)
                            purchases.append(
                                [
                                    str(store[0]),
                                    str(store[4]),
                                    str(intAmount),
                                    str(store[5]),
                                    str(store[2]),
                                ]
                            )
                            intAmount -= intAmount
                            if intAmount <= 0:
                                break
                    else:  # Not in the region
                        continue

                else:  # Out of region
                    if intAmount >= float(store[3]):
                        query = (
                            "UPDATE Inventory SET Amount = Amount -"
                            + str(store[3])
                            + " WHERE store_id = "
                            + str(store[0])
                            + " AND UPC_Code = "
                            + str(store[4])
                            + ";"
                        )
                        cursor.execute(query)
                        purchases.append(
                            [
                                str(store[0]),
                                str(store[4]),
                                str(store[3]),
                                str(store[5]),
                                str(store[2]),
                            ]
                        )
                        intAmount -= int(store[3])
                        usedStoreIDs.append(int(store[0]))
                        if intAmount <= 0:
                            break

                    else:
                        query = (
                            "UPDATE Inventory SET Amount = Amount -"
                            + str(intAmount)
                            + " WHERE store_id = "
                            + str(store[0])
                            + " AND UPC_Code = "
                            + str(store[4])
                            + ";"
                        )
                        cursor.execute(query)
                        purchases.append(
                            [
                                str(store[0]),
                                str(store[4]),
                                str(intAmount),
                                str(store[5]),
                                str(store[2]),
                            ]
                        )
                        intAmount -= intAmount
                        if intAmount <= 0:
                            break
            inRegion = False
            index += 1
            if index > 1:  # Break if quanity changes during run
                break
            if intAmount <= 0:
                break
    except mysql.connector.Error as error:
        print("Error caught on query, rolling back database")
        print("Error: ", error)
        cnx.rollback()  # Roll back
    return purchases


def multiPurchase(login, avalibleProductsParam):
    cursor.execute("START TRANSACTION")
    try:
        activePurchase = True
        allPurchases = [[[]]]
        while activePurchase:
            avalibleProducts = webOrderMenu(avalibleProductsParam)
            try:
                if avalibleProducts == -1:
                    continue
                elif len(avalibleProducts) == 0:
                    activePurchase = False
                    break
            except:
                activePurchase = False
                break
            purchase = purchaseProduct(login, avalibleProducts)
            for i in range(0, len(avalibleProductsParam)):
                if str(avalibleProductsParam[i][2]) == str(purchase[1][1]):
                    avalibleProductsParam.pop(i)
                    break
            allPurchases.append(purchase)
            choice = input("Would you like to purchase any additional products? Yes/No")
            if choice.lower() == "no":
                activePurchase = False
                break
        # Handle sales
        # Sort by store id
        allAllPurchases = [[]]
        allAllPurchases.pop(0)
        for purchase in allPurchases:
            for innerPurchase in purchase:
                if innerPurchase != []:
                    allAllPurchases.append(innerPurchase)
        allAllPurchases = sorted(allAllPurchases, key=lambda x: x[0])  # sort purchases
        currentStoreId = -1
        currentSaleID = -1
        for purchase in allAllPurchases:  # Add to exisitng sale
            if purchase[0] == currentStoreId:
                addSaleItem(purchase[1], purchase[2], currentSaleID, purchase[3])
            else:
                # NewSale
                currentStoreId = purchase[0]
                currentSaleID = addSale(login, purchase[0], "Online")
                if currentSaleID != -1:
                    addSaleItem(purchase[1], purchase[2], currentSaleID, purchase[3])
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
    if len(allPurchases) == 0:
        print("No Purchases")
    else:
        allAllPurchases = sorted(allPurchases, key=lambda x: x[1])  # sort purchases
        print("Purchase Summary: ")
        # ID, UPC, Amount, Price, Product_name
        totalProduct = 0
        currentProductUPC = int(allAllPurchases[0][1])
        for i in range(0, len(allAllPurchases)):
            if int(allAllPurchases[i][1]) == currentProductUPC:
                totalProduct += int(allAllPurchases[i][2])
            else:
                print(
                    "Product: "
                    + str(allAllPurchases[i - 1][4])
                    + " Quantity: "
                    + str(totalProduct)
                    + " Total Cost: "
                    + str(totalProduct * int(allAllPurchases[i - 1][3]))
                )
                totalProduct = 0
                currentProductUPC = int(allAllPurchases[i][1])
                totalProduct += int(allAllPurchases[i][2])
        print(
            "Product: "
            + str(allAllPurchases[len(allAllPurchases) - 1][4])
            + " Quantity: "
            + str(totalProduct)
            + " Total Cost: "
            + str(totalProduct * int(allAllPurchases[len(allAllPurchases) - 1][3]))
        )


def addSale(customer, store, status):  # Helper to add a sale to the database
    cursor.execute("START TRANSACTION")
    try:
        query = "SELECT IFNULL(MAX(Sale_ID), 0) + 1 FROM Sale;"
        cursor.execute(query)
        sale_id = int(cursor.fetchone()[0])
        query = (
            "INSERT INTO Sale (Sale_ID, Store_ID, Customer_ID, Date, Sale_Type) VALUES ("
            + str(sale_id)
            + ","
            + str(store)
            + ","
            + str(customer)
            + ", NOW(), '"
            + status
            + "'); "
        )
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
        query = (
            "INSERT INTO Sale_Item (Sale_ID, UPC_Code, Quanity, Local_Price) VALUES ("
            + str(SALE_ID)
            + ","
            + str(product_UPC)
            + ","
            + str(amount)
            + ","
            + str(price)
            + "); "
        )
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
    os.system("cls")

    firstName = input("First Name: ")

    lastName = input("Last Name: ")

    phone = input("phone number: ")

    validRegion = False
    while validRegion == False:
        r = input("Region:\n 1. North \n 2. South \n 3. East \n 4. West\n")
        try:
            region = int(r)
        except:
            input("Invalid region\n hit enter to retry")
            continue
        if region > 0 and region < 5:
            validRegion = True
        else:
            input("select a valid region\n hit enter to retry")

    uniqueID = False
    while uniqueID == False:
        customer_id = input("input a numeric customer id: ")
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
            insert = (
                "INSERT INTO Customer(Customer_ID, First_Name, Last_Name, Phone_Number,Region) Values ("
                + customer_id
                + ",'"
                + firstName
                + "','"
                + lastName
                + "','"
                + phone
                + "',"
                + str(region)
                + ");"
            )

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
    os.system("cls")
    store_id = input("Input Store ID: ")
    query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        store_id = input("Input Valid Store ID: ")
        query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")
    RESTOCK_AMOUNT = 20
    # Final all stores and products that need to be restocked
    # Query to find which products are low
    # query = """SELECT i.Store_ID, i.UPC_Code, i.Amount, s.Region
    #             FROM Inventory AS i
    #             JOIN Store AS s ON i.Store_ID = s.Store_ID
    #             WHERE i.Amount <= 5;"""
    query = (
        """SELECT i.Store_ID, i.UPC_Code, i.Amount, s.Region
                FROM Inventory AS i
                JOIN Store AS s ON i.Store_ID = s.Store_ID
                WHERE i.Amount <= 5
                AND s.Store_ID = """
        + store_id
        + """
                 AND i.UPC_Code NOT IN (
                    SELECT ri.UPC_Code
                    FROM Restock_Item AS ri
                    JOIN Restock AS r ON ri.Stocking_ID = r.Stocking_ID
                    WHERE r.Restock_Status = 'Placed'
                    AND r.Store_ID = s.Store_ID
                );"""
    )
    cursor.execute(query)
    restockProducts = cursor.fetchall()
    restockProducts = sorted(restockProducts, key=lambda x: x[0])  # sort purchases
    print("Items needing Restocking: ")
    for restock in restockProducts:
        print(
            "Store ID: "
            + str(restock[0])
            + " product UPC: "
            + str(restock[1])
            + " quantity: "
            + str(restock[2])
        )
    input("Press Enter to restock")
    # Subtract products from warehouse_inventories
    for product in restockProducts:
        query = (
            "SELECT i.Max_Capacity FROM Inventory as i WHERE i.Store_ID = "
            + str(product[0])
            + " AND i.UPC_Code ="
            + str(product[1])
        )

        cursor.execute(query)
        # Set Restock Amount to fill to max
        RESTOCK_AMOUNT = cursor.fetchall()[0][0] - product[2]
        query = (
            "UPDATE Warehouse_Inventory AS wi JOIN Warehouse AS w ON wi.Warehouse_ID = w.Warehouse_ID SET wi.Amount = wi.Amount - "
            + str(RESTOCK_AMOUNT)
            + " WHERE w.Region = '"
            + getRegion(product[3])
            + "' AND wi.UPC_Code = "
            + str(product[1])
            + ";"
        )
        cursor.execute(query)
    # Add Restock records
    currentStoreId = -1
    currentRestockID = -1
    for product in restockProducts:
        if product[0] == currentStoreId:  # Add to exisitng restock
            addRestockItem(product[1], RESTOCK_AMOUNT, currentRestockID)
        else:
            # New Restock
            currentStoreId = product[0]
            currentRestockID = addRestock(product[0], product[3])
            if currentRestockID != -1:
                addRestockItem(product[1], RESTOCK_AMOUNT, currentRestockID)
            else:
                print("Error in making restock, please try again")
                cnx.rollback()
                break
    # printRestocks() #Uncomment to display all Restock and Restock Items
    print("Restocking Complete")
    cnx.commit()


def getRegion(i):
    if i == 1:
        return "North"
    if i == 2:
        return "South"
    if i == 3:
        return "East"
    if i == 4:
        return "West"


def stock():
    # store login
    os.system("cls")
    store_id = input("Input Store ID: ")
    query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        store_id = input("Input Valid Store ID: ")
        query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")

    # print list of products possible to stock
    query = """ SELECT
                p.UPC_Code,
                p.Name,
                s.Region
                FROM Inventory AS i
                JOIN Product AS p ON i.UPC_Code = p.UPC_Code
                JOIN Store AS s ON i.Store_ID = s.Store_ID
                WHERE i.Amount < i.Max_Capacity
                AND i.Store_ID = """ + str(
        store_id
    )
    cursor.execute(query)
    avaliable_products = cursor.fetchall()
    allOrders = multiStock(store_id, avaliable_products)

    restock_id = -1
    restock_id = addRestock(store_id, avaliable_products[0][2])
    for order in allOrders:
        # query = "SELECT wi.Max_Capacity FROM Warehouse_Inventory as wi WHERE wi.Warehouse_ID = " + \
        #     str(product[3])
        # cursor.execute(query)
        RESTOCK_AMOUNT = order[2]
        addRestockItem(order[0], RESTOCK_AMOUNT, restock_id)
    cnx.commit()


def multiStock(login, avalibleProducts):
    activeStock = True
    allStocks = []
    while activeStock:
        order = stockProduct(login, avalibleProducts)
        for i in range(0, len(avalibleProducts)):
            # print(avalibleProducts[i][2])
            # print(purchase[1][1])
            if str(avalibleProducts[i][0]) == str(order[0]):
                avalibleProducts.pop(i)
                break
        allStocks.append(order)
        choice = input("Would you like to purchase any additional products? Yes/No")
        if choice.lower() == "no":
            activeStock = False
            break

    return allStocks


def stockProduct(wlogin, avaliable_products):
    validSelection = False
    validAmount = False
    while (not validSelection) or (not validAmount):
        index = 0
        for product in avaliable_products:
            query = (
                """SELECT (Max_Capacity - Amount) AS Available_Capacity
                    FROM Inventory
                    WHERE UPC_Code = """
                + str(product[0])
                + " AND Store_ID = "
                + wlogin
                + ";"
            )
            cursor.execute(query)
            capacity = cursor.fetchall()
            print(
                "Product "
                + str(index)
                + ": "
                + str(product[1])
                + " Quantity Avalible for Purchase: "
                + str(capacity[0][0])
            )
            index += 1
        product_selection = input(
            "Enter the number corresponding to the product you want to stock: \n"
        )
        try:
            if (
                int(product_selection) > len(avaliable_products) - 1
                or int(product_selection) < 0
            ):
                input("Not a valid product please press enter to try again")
                continue
            else:
                validSelection = True
        except:
            input("Not a valid product please press enter to try again")
            continue
        amount = input("Enter the amount you want to stock: \n")

        try:
            intAmount = int(amount)
            if intAmount > float(capacity[0][0]):
                input("Not enough storage for that product, Press enter to retry")
                continue
            else:
                validAmount = True
        except:
            input("Invalid amount please press enter to try again")
            continue

    stock = [
        avaliable_products[int(product_selection)][0],
        avaliable_products[int(product_selection)][2],
        intAmount,
    ]

    return stock


def addRestock(store, warehouse):  # Helper to add a restock to the database
    cursor.execute("START TRANSACTION")
    try:
        now = datetime.datetime.now()
        current_hour = now.hour
        current_minute = now.minute
        query = "SELECT IFNULL(MAX(Stocking_ID), 0) + 1 FROM Restock;"
        cursor.execute(query)
        Stocking_ID = int(cursor.fetchone()[0])
        query = (
            "INSERT INTO Restock (Stocking_ID, Store_ID, Warehouse_ID, Date, Time_Hour, Time_Minute, Restock_Status) VALUES ("
            + str(Stocking_ID)
            + ","
            + str(store)
            + ","
            + str(warehouse)
            + ", NOW() ,"
            + str(current_hour)
            + ","
            + str(current_minute)
            + ", 'Placed'"
            + "); "
        )
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
        query = (
            "INSERT INTO Restock_Item (STOCKING_ID, UPC_Code, Quantity) VALUES ("
            + str(STOCKING_ID)
            + ","
            + str(product_UPC)
            + ","
            + str(amount)
            + "); "
        )
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
    os.system("cls")
    warehouse_id = input("Input Warehouse ID: ")
    query = "SELECT * FROM Warehouse WHERE Warehouse_ID =" + warehouse_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        warehouse_id = input("Input Valid Warehouse ID: ")
        query = "SELECT * FROM Warehouse WHERE Warehouse_ID =" + warehouse_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")
    REORDER_AMOUNT = 50
    os.system("cls")

    query = (
        """  SELECT wi.UPC_Code, sb.Vendor_ID, wi.Amount, wi.Warehouse_ID
            FROM Warehouse_Inventory AS wi
            JOIN Supplied_By AS sb ON wi.UPC_Code = sb.UPC_Code
            JOIN Warehouse AS w ON wi.Warehouse_ID = w.Warehouse_ID
            WHERE wi.Warehouse_ID ="""
        + str(warehouse_id)
        + """ AND wi.Amount < 100
            AND wi.UPC_Code NOT IN (
                SELECT ri.UPC_Code
                FROM Reorder_Item AS ri
                JOIN Reorder AS r ON ri.Reorder_ID = r.Reorder_ID
                WHERE r.Reorder_Status = 'ORDERED'
                AND r.Warehouse_ID ="""
        + str(warehouse_id)
        + """
                UNION
                SELECT si.UPC_Code
                FROM Shipment_Item AS si
                JOIN Shipment AS sh ON si.Shipment_ID = sh.Shipment_ID
                WHERE sh.Shipment_Status = 1
                AND sh.Warehouse_ID ="""
        + str(warehouse_id)
        + ");"
    )
    cursor.execute(query)
    reorderProducts = cursor.fetchall()
    reorderProducts = sorted(
        reorderProducts, key=lambda x: x[1]
    )  # sort products by vendor
    if len(reorderProducts) == 0:
        print("Warehouse " + str(warehouse_id) + " is fully stocked.")
    else:
        print("Items needing Reordering: ")
        for product in reorderProducts:
            print(
                "Warehouse ID: "
                + str(warehouse_id)
                + " product UPC: "
                + str(product[0])
                + " quantity: "
                + str(product[2])
                + " Vendor ID: "
                + str(product[1])
            )
        input("Press Enter to reorder")

    currVendor = -1
    reorder_id = -2
    for product in reorderProducts:
        query = (
            "SELECT wi.Max_Capacity FROM Warehouse_Inventory as wi WHERE wi.Warehouse_ID = "
            + str(product[3])
        )
        cursor.execute(query)
        # Set Restock Amount to fill to max
        REORDER_AMOUNT = cursor.fetchall()[0][0] - product[2]
        vendorId = product[1]

        if vendorId != currVendor:
            # create new reorder, add curr product
            reorder_id = addReorder(warehouse_id, vendorId)
            currVendor = vendorId
            addReorderItem(product[0], REORDER_AMOUNT, reorder_id)
            cnx.commit()
        else:
            # add to curr reorder
            addReorderItem(product[0], REORDER_AMOUNT, reorder_id)
            cnx.commit()


def order():
    # warehouse login
    os.system("cls")
    warehouse_id = input("Input Warehouse ID: ")
    query = "SELECT * FROM Warehouse WHERE Warehouse_ID =" + warehouse_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        warehouse_id = input("Input Valid Warehouse ID: ")
        query = "SELECT * FROM Warehouse WHERE Warehouse_ID =" + warehouse_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")

    # print list of products possible to order
    query = (
        """ SELECT
            p.UPC_Code,
            p.Name AS Product_Name,
            v.Vendor_ID,
            v.Name AS Vendor_Name
            FROM Product AS p
            JOIN Supplied_By AS sb ON p.UPC_Code = sb.UPC_Code
            JOIN Vendor AS v ON sb.Vendor_ID = v.Vendor_ID
            JOIN Warehouse_Inventory AS wi ON p.UPC_Code = wi.UPC_Code
            WHERE wi.Warehouse_ID = """
        + warehouse_id
        + " AND wi.Amount < wi.Max_Capacity ORDER BY p.UPC_Code, v.Vendor_ID;"
    )
    cursor.execute(query)
    avaliable_products = cursor.fetchall()
    allOrders = multiOrder(warehouse_id, avaliable_products)

    currVendor = -1
    reorder_id = -2
    for order in allOrders:
        # query = "SELECT wi.Max_Capacity FROM Warehouse_Inventory as wi WHERE wi.Warehouse_ID = " + \
        #     str(product[3])
        # cursor.execute(query)

        REORDER_AMOUNT = order[2]
        print(REORDER_AMOUNT)
        vendorId = order[1]

        if vendorId != currVendor:
            # create new reorder, add curr product
            reorder_id = addReorder(warehouse_id, vendorId)
            currVendor = vendorId
            addReorderItem(order[0], REORDER_AMOUNT, reorder_id)
            cnx.commit()
        else:
            # add to curr reorder
            addReorderItem(order[0], REORDER_AMOUNT, reorder_id)
            cnx.commit()


def orderProduct(wlogin, avaliable_products):
    validSelection = False
    validAmount = False
    while (not validSelection) or (not validAmount):
        index = 0
        for product in avaliable_products:
            query = (
                """SELECT (Max_Capacity - Amount) AS Available_Capacity
                    FROM Warehouse_Inventory
                    WHERE UPC_Code = """
                + str(product[0])
                + " AND Warehouse_ID = "
                + wlogin
                + ";"
            )
            cursor.execute(query)
            capacity = cursor.fetchall()
            print(
                "Product "
                + str(index)
                + ": "
                + str(product[1])
                + " Quantity Avalible for Purchase: "
                + str(capacity[0][0])
            )
            index += 1
        product_selection = input(
            "Enter the number corresponding to the product you want to stock: \n"
        )
        try:
            if (
                int(product_selection) > len(avaliable_products) - 1
                or int(product_selection) < 0
            ):
                input("Not a valid product please press enter to try again")
                continue
            else:
                validSelection = True
        except:
            input("Not a valid product please press enter to try again")
            continue
        amount = input("Enter the amount you want to stock: \n")

        try:
            intAmount = int(amount)
            if intAmount > float(capacity[0][0]):
                input("Not enough storage for that product, Press enter to retry")
                continue
            else:
                validAmount = True
        except:
            input("Invalid amount please press enter to try again")
            continue

    order = [
        avaliable_products[int(product_selection)][0],
        avaliable_products[int(product_selection)][2],
        intAmount,
    ]

    return order


def multiOrder(login, avalibleProducts):
    activeOrder = True
    allOrders = []
    while activeOrder:
        order = orderProduct(login, avalibleProducts)
        for i in range(0, len(avalibleProducts)):
            # print(avalibleProducts[i][2])
            # print(purchase[1][1])
            if str(avalibleProducts[i][0]) == str(order[0]):
                avalibleProducts.pop(i)
                break
        allOrders.append(order)
        choice = input("Would you like to purchase any additional products? Yes/No")
        if choice.lower() == "no":
            activePurchase = False
            break

    return allOrders


def addReorder(warehouse_id, vendor_id):
    cursor.execute("START TRANSACTION")
    try:
        query = "SELECT IFNULL(MAX(Reorder_ID), 0) + 1 FROM Reorder;"
        cursor.execute(query)
        Reorder_ID = int(cursor.fetchone()[0])
        query = (
            "INSERT INTO Reorder (Reorder_ID, Warehouse_ID, Vendor_ID, Reorder_Status) VALUES ("
            + str(Reorder_ID)
            + ","
            + str(warehouse_id)
            + ","
            + str(vendor_id)
            + ",'ORDERED'); "
        )
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
        query = (
            "INSERT INTO Reorder_Item (Reorder_ID, UPC_Code, Amount) VALUES ("
            + str(reorder_id)
            + ","
            + str(product_UPC)
            + ","
            + str(amount)
            + "); "
        )
        cursor.execute(query)
        # return True
    except mysql.connector.Error as error:
        print("Error caught on query, rolling back database")
        print("Error: ", error)
        cnx.rollback()  # Roll back
        # return False


def shipment():
    os.system("cls")
    vendor_id = input("Input Vendor ID: ")
    query = "SELECT * FROM Vendor WHERE Vendor_ID =" + vendor_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        vendor_id = input("Input Valid Vendor ID: ")
        query = "SELECT * FROM Vendor WHERE Vendor_ID =" + vendor_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            print(error)
            input("\npress enter to continue\n")
    os.system("cls")

    # query = "SELECT DISTINCT Vendor_ID FROM Vendor WHERE Vendor_ID = " + vendor_id + ";"
    # cursor.execute(query)
    # vendors = cursor.fetchall()

    query = (
        "SELECT * FROM Reorder WHERE Vendor_ID ="
        + vendor_id
        + " AND Reorder_Status = 'ORDERED';"
    )
    cursor.execute(query)
    reorders = cursor.fetchall()
    print("Vendor " + str(vendor_id) + " shipments: ")
    for order in reorders:
        query = "SELECT * FROM Reorder_Item WHERE Reorder_ID =" + str(order[0]) + ";"
        cursor.execute(query)
        products = cursor.fetchall()

        shipment_id = addShipment(order[2], vendor_id)
        query = (
            "UPDATE Reorder SET Reorder_Status = 'Completed' WHERE Reorder_ID = "
            + str(order[0])
            + "; "
        )
        cursor.execute(query)
        for product in products:
            addShipmentItem(product[1], product[0], shipment_id)
            print("Order " + str(order[0]) + " to warehouse " + str(order[2]))
            cnx.commit()

    input("")


def addShipment(warehouse, vendor):
    cursor.execute("START TRANSACTION")
    try:
        now = datetime.datetime.now()
        current_hour = now.hour
        current_minute = now.minute
        query = "SELECT IFNULL(MAX(Shipment_ID), 0) + 1 FROM Shipment;"
        cursor.execute(query)
        Shipment_ID = int(cursor.fetchone()[0])
        validDate = False
        date_str = ""
        while not validDate:
            try:
                deliveryDay = input(
                    "Please enter the delivery day for Shipment: "
                    + str(Shipment_ID)
                    + " to warehouse: "
                    + str(warehouse)
                    + " "
                )
                deliveryMonth = input("Delivery Month: ")
                deliveryYear = input("Delivery Year: ")
                deliveryHour = input("Delivery Hour: ")
                deliveryMinute = input("Delivery Minute: ")
                date = datetime.datetime(
                    int(deliveryYear),
                    int(deliveryMonth),
                    int(deliveryDay),
                    hour=int(deliveryHour),
                    minute=int(deliveryMinute),
                )
                dateOnly = datetime.date(
                    int(deliveryYear), int(deliveryMonth), int(deliveryDay)
                )
                date_str = dateOnly.strftime("%Y-%m-%d")
                if date < now:
                    print(
                        "Date and time is in the past, please enter a valid date and time"
                    )
                    continue
                else:
                    validDate = True
            except:
                print("Invalid entry please try again")
                continue
        query = (
            "INSERT INTO Shipment (Shipment_ID, Vendor_ID, Warehouse_ID, Shipment_Date, Time_Hour, Time_Minute, Shipment_Status) VALUES ("
            + str(Shipment_ID)
            + ","
            + str(vendor)
            + ","
            + str(warehouse)
            + ", '"
            + str(date_str)
            + "', "
            + str(deliveryHour)
            + ", "
            + str(deliveryMinute)
            + ", '1'"
            + "); "
        )
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
        query = (
            "INSERT INTO Shipment_Item (Shipment_ID, UPC_Code, Quantity) VALUES ("
            + str(Shipment_ID)
            + ","
            + str(product_UPC)
            + ","
            + str(amount)
            + "); "
        )

        cursor.execute(query)
        return True
    except mysql.connector.Error as error:
        print("Error caught on query, rolling back database")
        print("Error: ", error)
        cnx.rollback()  # Roll back
        return False


def updateInventory():
    # Find all Pending Restock
    os.system("cls")
    store_id = input("Input Store ID: ")
    query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        store_id = input("Input Valid Store ID: ")
        query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")

    query = (
        "SELECT * FROM Restock WHERE Restock_Status = 'Placed' AND Store_ID ="
        + store_id
        + ";"
    )
    cursor.execute(query)
    allRestocks = cursor.fetchall()
    now = datetime.datetime.now()
    print("Restocks arrived since last check: ")
    for restock in allRestocks:
        restockHour = restock[2]
        restockMinute = restock[3]
        time_obj = datetime.time(restockHour, restockMinute)
        date_obj = datetime.datetime.combine(restock[1], time_obj)
        if now > date_obj:
            print(
                "ID: "
                + str(restock[0])
                + " Store: "
                + str(restock[5])
                + " Warehouse: "
                + str(restock[6])
            )
    if len(allRestocks) != 0:
        print("Updating store inventories...")
        for restock in allRestocks:
            query = (
                "SELECT * FROM Restock_Item WHERE Stocking_ID = "
                + str(restock[0])
                + "; "
            )
            cursor.execute(query)
            restockItems = cursor.fetchall()
            for item in restockItems:
                query = (
                    "UPDATE Inventory SET Amount = Amount +"
                    + str(item[0])
                    + " WHERE store_id = "
                    + str(restock[5])
                    + " AND UPC_Code = "
                    + str(item[2])
                    + ";"
                )
                cursor.execute(query)
            query = (
                "UPDATE Restock SET Restock_Status = 'Completed' WHERE Stocking_ID = "
                + str(restock[0])
                + "; "
            )
            cursor.execute(query)
        print("Updated\n")
    cnx.commit()
    input("")
    os.system("cls")


def updateWarehouseInventory():
    os.system("cls")
    warehouse_id = input("Input Warehouse ID: ")
    query = "SELECT * FROM Warehouse WHERE Warehouse_ID =" + warehouse_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        warehouse_id = input("Input Valid Warehouse ID: ")
        query = "SELECT * FROM Warehouse WHERE Warehouse_ID =" + warehouse_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")
    os.system("cls")
    query = (
        "SELECT * FROM Shipment WHERE Shipment_Status = 1 and Warehouse_ID = "
        + warehouse_id
        + ";"
    )
    cursor.execute(query)
    allShipments = cursor.fetchall()
    now = datetime.datetime.now()
    print("Shipments arrived since last check: ")
    if len(allShipments) != 0:
        print("Updating warehouse inventories...")
        for shipment in allShipments:
            shipmentHour = shipment[2]
            shipmentMinute = shipment[3]
            time_obj = datetime.time(shipmentHour, shipmentMinute)
            date_obj = datetime.datetime.combine(shipment[1], time_obj)
            if now > date_obj:
                print(
                    "ID: "
                    + str(shipment[0])
                    + " Warehouse: "
                    + str(shipment[6])
                    + " Vendor: "
                    + str(shipment[5])
                )
                query = (
                    "SELECT * FROM Shipment_Item WHERE Shipment_ID = "
                    + str(shipment[0])
                    + "; "
                )
                cursor.execute(query)
                shipmentItems = cursor.fetchall()
                for item in shipmentItems:
                    query = (
                        "UPDATE Warehouse_Inventory SET Amount = Amount +"
                        + str(item[0])
                        + " WHERE warehouse_id = "
                        + str(shipment[6])
                        + " AND UPC_Code = "
                        + str(item[1])
                        + ";"
                    )
                    cursor.execute(query)
                query = (
                    "UPDATE Shipment SET Shipment_Status = 0 WHERE Shipment_ID = "
                    + str(shipment[0])
                    + "; "
                )
                cursor.execute(query)
        print("Updated\n")
    cnx.commit()
    input("")
    os.system("cls")


def purchaseHistory():
    os.system("cls")

    login = input("input ur id to login or -1 to register: \n")
    # check if customer exists in database
    query = "SELECT * FROM Customer WHERE Customer_ID = " + login
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    if not cursor.fetchone():
        # no id
        login = register()
    query = (
        """
    SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
	s.date,
	si.UPC_Code,
	p.name,
    si.Local_Price,
	si.Quanity,
    s.Sale_Type
    FROM
	Customer c, Sale s, Sale_Item si, Product p
    WHERE
	c.customer_id = s.customer_id AND
	s.sale_id = si.sale_id AND
	si.UPC_Code = p.UPC_Code AND
	c.customer_id = """
        + login
        + " ORDER BY s.sale_id ASC, si.UPC_Code "
    )
    cursor.execute(query)
    purchases = cursor.fetchall()
    print(purchases[0][1] + " " + purchases[0][2] + "'s Purchase History: ")
    for purchase in purchases:
        formatted_date = purchase[3].strftime("%B %d, %Y")
        print(
            formatted_date
            + " Product: "
            + purchase[5]
            + " Quantity: "
            + str(purchase[7])
            + " Cost Per Item: $"
            + str(purchase[6])
            + " Total Cost: $"
            + str(purchase[6] * purchase[7]),
            " Sale Type: " + purchase[8],
        )


def salesHistory():
    # store login
    os.system("cls")
    store_id = input("Input Store ID: ")
    query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        store_id = input("Input Valid Store ID: ")
        query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")
    query = (
        """
    SELECT
    s.Sale_ID,
    s.Store_ID,
    s.Date,
    s.Customer_ID,
    c.First_Name AS Customer_Name_First,
    c.Last_Name AS Customer_Name_Last,
    si.UPC_Code,
    p.Name AS Product_Name,
    si.Quanity,
    si.Local_Price,
    s.Sale_Type
FROM Sale AS s
JOIN Sale_Item AS si ON s.Sale_ID = si.Sale_ID
JOIN Product AS p ON si.UPC_Code = p.UPC_Code
JOIN Customer AS c ON s.Customer_ID = c.Customer_ID
WHERE s.Store_ID = """
        + store_id
        + " ORDER BY s.Sale_ID ASC;"
    )

    cursor.execute(query)
    sales = cursor.fetchall()
    print("Stores: " + str(store_id) + "'s sales history")
    for sale in sales:
        formatted_date = sale[2].strftime("%B %d, %Y")
        print(
            formatted_date
            + ": Product: ("
            + str(sale[6])
            + ") "
            + sale[7]
            + " Quantity: "
            + str(sale[8])
            + " Cost Per Item: $"
            + str(sale[9])
            + " Total Cost: $"
            + str(sale[8] * sale[9])
            + " Buyer: "
            + sale[4]
            + " "
            + sale[5]
            + " Sale Type: "
            + sale[10]
        )
    input("Press enter to contiune")


# checkout - update inventory and customer frequent buys


def checkout():
    activeRegister = True
    # input: customer info ,  product id and quantity , store id
    # store login
    os.system("cls")
    store_id = input("Input Store ID: ")
    query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        input(error + "\npress enter to continue\n")

    while not cursor.fetchone():
        os.system("cls")
        store_id = input("Input Valid Store ID: ")
        query = "SELECT * FROM Store WHERE Store_ID =" + store_id + ";"
        try:
            cursor.execute(query)
        except mysql.connector.Error as error:
            input(error + "\npress enter to continue\n")
    while activeRegister:
        saleOngoing = True
        allSales = []
        while saleOngoing:
            item = input("Scan Item: (-1 to Finish, -10 to close register)")
            if item == str(-1):
                saleOngoing = False
                break
            elif item == str(-10):
                saleOngoing = False
                activeRegister = False
                return
            query = "SELECT * FROM Product WHERE UPC_Code = " + str(item)
            cursor.execute(query)
            if len(cursor.fetchall()) == 0:  # Invalid Product Scanned
                print("Invalid UPC Code")
            else:
                allSales.append(item)
        if len(allSales) == 0:
            continue
        # Get customer info:
        info = input("Does customer want to provide info? Yes/No\n")
        id = -999
        if info.lower() != "no":
            # Check if they exist
            id = input("input ur id to login or -1 to register: \n")
            # check if customer exists in database
            query = "SELECT * FROM Customer WHERE Customer_ID = " + id
            try:
                cursor.execute(query)
            except mysql.connector.Error as error:
                input(error + "\npress enter to continue\n")
            if not cursor.fetchone():
                # no id
                input("Not a Valid ID, press enter to register")
                id = register()
        # Handle Sales
        sale_id = addSale(id, store_id, "In_person")
        allSales.sort()
        quantity = 0
        currentUPC = allSales[0]
        cursor.execute("START TRANSACTION")
        totalCost = 0
        try:
            for sale in allSales:
                if currentUPC == sale:
                    quantity += 1
                else:
                    query = (
                        "SELECT Local_Price FROM Inventory WHERE UPC_Code = "
                        + str(sale)
                        + " AND Store_ID = "
                        + str(store_id)
                        + ";"
                    )
                    cursor.execute(query)
                    price = cursor.fetchall()[0][0]
                    addSaleItem(currentUPC, quantity, sale_id, price)
                    quantity = 1
                    currentUPC = sale
                query = (
                    "UPDATE Inventory SET Amount = Amount - 1 WHERE Store_ID = "
                    + store_id
                    + " AND UPC_Code = "
                    + str(sale)
                    + ";"
                )
                cursor.execute(query)
            query = (
                "SELECT Local_Price FROM Inventory WHERE UPC_Code = "
                + str(sale)
                + " AND Store_ID = "
                + str(store_id)
                + ";"
            )
            cursor.execute(query)
            price = cursor.fetchall()[0][0]
            totalCost += int(price) * int(quantity)
            addSaleItem(currentUPC, quantity, sale_id, price)
        except mysql.connector.Error as error:
            print(
                "Error caught on query, rolling back database, please redo transaction"
            )
            print("Error: ", error)
            cnx.rollback()  # Roll back
        print("Completed Purchase total cost: " + str(totalCost))
        cnx.commit()


def main():
    runMainMenu()


main()
