#database interfaces 
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
            os.system('cls')
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
#OLAP
def OLAP():
    os.system('cls')
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
            #Total inventory value per store and region:
            query ="""SELECT s.Region, s.Store_ID, SUM(i.Amount * i.Local_Price) as Total_Inventory_Value
                        FROM Store s
                        JOIN Inventory i ON s.Store_ID = i.Store_ID
                        GROUP BY s.Region, s.Store_ID
                        WITH ROLLUP;"""
            

        case 2: 
            #Total products supplied by each vendor, broken down by region:
            query="""SELECT v.Region, v.Name as Vendor_Name, COUNT(DISTINCT sb.UPC_Code) as Total_Products
                    FROM Vendor v
                    JOIN Supplied_By sb ON v.Vendor_ID = sb.Vendor_ID
                    JOIN Product p ON sb.UPC_Code = p.UPC_Code
                    JOIN Warehouse_Inventory wi ON p.UPC_Code = wi.UPC_Code
                    JOIN Warehouse w ON wi.Warehouse_ID = w.Warehouse_ID
                    GROUP BY v.Region, v.Name
                    WITH ROLLUP;"""
        case 3: 
               #Average inventory levels for each product type by region:
                query="""SELECT w.Region, p.Product_Type, AVG(i.Amount) as Avg_Inventory
                        FROM Warehouse w
                        JOIN Warehouse_Inventory i ON w.Warehouse_ID = i.Warehouse_ID
                        JOIN Product p ON i.UPC_Code = p.UPC_Code
                        GROUP BY w.Region, p.Product_Type
                        WITH ROLLUP;"""
        case 4: 
              #Top 10 customers by total sales in each region:
                query ="""WITH CustomerSalesByRegion AS (
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
              #best sellers
              query =""" WITH SalesByRegion AS (
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

   

#web orders
def webOrder(): 
    #input: location, products, quant (check if products are in closest store, )
    login = input("input ur id to login or -1 to register: \n")
    #check in customer exists in database
    query="SELECT * FROM Customer WHERE Customer_ID = " + login
    try: 
        cursor.execute(query)
    except mysql.connector.Error as error: 
         input(error + "\npress enter to continue\n")

    if not cursor.fetchone():
         #no id
         login = register()
    
    query = "SELECT Region FROM Customer WHERE Customer_id=" + login
    cursor.execute(query)
    customerRegion = cursor.fetchall()

    query = """ 
              

                """
    
    cursor.execute(query) 
    products = cursor.fetchall()
    

        

def register():
    print("")
    os.system('cls')
    firstName = input("First Name: ") 
    
    lastName = input("Last Name: ")
   
    phone = input('phone number: ')
   
    validRegion = False
    while validRegion == False: 
        nregion = input('Region:\n 1. North \n 2. South \n 3. East \n 4. West\n')
        if int(nregion) == 1:
                region = 'North'
                validRegion = True
        elif int(nregion) ==2:
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
        query="SELECT * FROM Customer WHERE Customer_ID = " + customer_id 
        try: 
            cursor.execute(query)
        except mysql.connector.Error as error: 
            input(error + "\npress enter to continue\n")

        if cursor.fetchone():
            #id exists
            input("id exists \n hit enter to try again")

        else: 
            uniqueID = True
            insert = "INSERT INTO Customer(Customer_ID, First_Name, Last_Name, Phone_Number) Values ("+customer_id+',\''+firstName+'\',\''+lastName+'\',\''+phone+'\');'
                        
            try:
                cursor.execute("START TRANSACTION") #Start a transaction so we can roll back if an error occurs
                try:
                    cursor.execute(insert)
                except mysql.connector.Error as error:
                    print("Error caught on query, rolling back database")
                    print("Error: ", error)
                    cnx.rollback() #Roll back
                    break
                
            except mysql.connector.Error as error: 
                print(error)
                input( "\npress enter to continue\n")

    return customer_id    

    



# reorder
def reorder():
    #input: store id (run to check for low stock and put in a reorder to nescessary vendor(s))
    input()

#vendor reorder shipment
def vendorShipment():
    #input: vendor_id (run to check for request to the vendor )
    input()
#update inventory from shipment 
def updateInventory():
    #input: store id ( run to check if shipments needs handling at the store )
        #return any requests 
            #input: order fullfillment with shipment date  
    input()

#checkout - update inventory and customer frequent buys 
def checkout():
    #input: customer info ,  product id and quantity , store id 
    input()

def main(): 
    runMainMenu()

main()
