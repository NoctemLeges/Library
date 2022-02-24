'''
1.Populate the member table and write required functions
2.Write the borrow functionality 
    add the quantity manipulation
3.Write the return functionality
'''
#-----------------------IMPORTING-------------------------------------------
import mysql.connector
mycon = mysql.connector.connect(host='localhost',user='user',passwd='nlccu086',database='library',auth_plugin='mysql_native_password')
mycursor=mycon.cursor()
#--------------------REQUIRED FUNCTIONS--------------------------------------
def generateMID():
    query = "select * from Members"
    mycursor.execute(query)
    data = mycursor.fetchall()
    if bool(data)==False:
        return '1'
    else:
        return len(data)+1
def generateAID():
    query = "select * from BookRecord"
    mycursor.execute(query)
    data = mycursor.fetchall()
    if bool(data)==False:
        return '1'
    else:
        return len(data)+1
def generateDOR(DOB):
    query = "select DATE_ADD('{DATE}', INTERVAL 30 DAY)".format(DATE=DOB)
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data[0][0]
def addMember(MName,Contact,Address):
    MID = generateMID()
    query = "insert into Members values('{MID}','{MNAME}','{Contact}','{ADDRESS}')".format(MID=MID,MNAME=MName,Contact=Contact,ADDRESS=Address)
    mycursor.execute(query)
    mycon.commit()
    print("SUCCESS!")
def borrowBook(MID,BID,DOB):
    AID = generateAID()
    DOR = generateDOR(DOB)
    query = "insert into BookRecord values('{AID}','{BID}','{MID}','{DOB}','{DOR}','{ACTION}')".format(AID=AID,BID=BID,MID=MID,DOB=DOB,DOR=DOR,ACTION='BORROW')
    mycursor.execute(query)
    mycon.commit()
    query_for_finding_quantity = "select * from BookStock where BookID='{}'".format(BID)
    mycursor.execute(query_for_finding_quantity)
    data = mycursor.fetchall()
    quantity = data[0][2]
    query_for_updating_quantity = "update BookStock set quantity='{}' where BookID='{}'".format(quantity-1,BID)
    mycursor.execute(query_for_updating_quantity)
    mycon.commit()
    print("SUCCESS!")
def returnBook(MID,BID,DOR):
    AID = generateAID()
    query ="insert into BookRecord values('{AID}','{BID}','{MID}',NULL,'{DOR}','{ACTION}')".format(AID=AID,BID=BID,MID=MID,DOR=DOR,ACTION='RETURN')
    mycursor.execute(query)
    mycon.commit()
    print("SUCESS!")
    query_for_finding_quantity = "select * from BookStock where BookID='{}'".format(BID)
    mycursor.execute(query_for_finding_quantity)
    data = mycursor.fetchall()
    quantity = data[0][2]
    query_for_updating_quantity="update BookStock set Quantity={} where BookID='{}'".format(quantity+1,BID)
    mycursor.execute(query_for_updating_quantity)
    mycon.commit()
def checkFine(MID,BID,DOR):
    query = "Select DOR from BookRecord where MemberID='{MID}' and BookID='{BID}' and Action='BORROW'".format(MID=MID,BID=BID)
    mycursor.execute(query)
    data = mycursor.fetchall()
    last = data[0][len(data)-1]
    query2 = "select '{DOR}'>'{date}'".format(DOR=last,date=DOR)
    mycursor.execute(query2)
    fine = mycursor.fetchall()
    return fine[0][0]
#----------------------------USER END-----------------------------------------
choice=int(input("1.Add Member\n2.Borrow book\n3.Return book\nEnter choice:"))

if choice==1:
    name = input("Enter member name:")
    contact = input("Enter member contact:")
    address = input("Enter member address:")
    addMember(name,contact,address)
if choice == 2:
    MID = input("Enter Member ID:")
    BID = input("Enter Book ID:")
    DOB = input("Enter date(yyyy-mm-dd):")
    borrowBook(MID,BID,DOB)
if choice == 3:
    MID = input("Enter Member ID:")
    BID = input("ENter Book ID:")
    DOR = input("Enter Date(yyyy-mm-dd):")
    fine = checkFine(MID,BID,DOR)
    if fine ==0:
        print('FINE')
        paid = input('FINE paid?(y/n):')
        if paid=='y':
            returnBook(MID,BID,DOR)
        else:
            print("PAY FINE")
    else:
        print("TIMELY")
        returnBook(MID,BID,DOR)
