import mysql.connector
def DataUpdate(name,branch): 
    mydb = mysql.connector.connect(user='root',host='localhost',passwd='rutuja',auth_plugin='mysql_native_password',database='recruitment_bot')
# conn = sql.connect(user='root',host='localhost',passwd='rutuja',auth_plugin='caching_sha2_password',database='test')
    mycursor = mydb.cursor() 

    if mydb.is_connected():
        print("success")
    else:
        print("fail")

    sql='INSERT INTO candidate_details (name, number) VALUES ("{0}","{1}");'.format(name,branch) 

    mycursor.execute(sql) 
    mydb.commit()
    print(mycursor.rowcount,"inserted")

if __name__=="__main__":
    DataUpdate("Nidhi","900458795")