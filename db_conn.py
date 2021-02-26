import mysql.connector
import random
def DataUpdate(name, number, last_name, branch, cgpa, email, lang): 
    mydb = mysql.connector.connect(user='root',host='localhost',passwd='rutuja',auth_plugin='mysql_native_password',database='recruitment_bot')
    mycursor = mydb.cursor() 

    # if mydb.is_connected():
    #     print("DataUpdate")
    # else:
    #     print("fail")

    sql='INSERT INTO candidate_details (name, number, last_name, branch, cgpa, email, lang) VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}");'.format(name, number, last_name, branch, cgpa, email, lang)
    mycursor.execute(sql) 
    mydb.commit()

def RetrieveCandidateId(email):
    mydb = mysql.connector.connect(user='root',host='localhost',passwd='rutuja',auth_plugin='mysql_native_password',database='recruitment_bot')
    mycursor = mydb.cursor() 

    # if mydb.is_connected():
    #     print("RetrieveCandidateId")
    # else:
    #     print("fail")

    sql='select cid from candidate_details where email="{0}";'.format(email)
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    return(myresult[0])


def QuestionHistory(cand_id,qid,level,concept,sim):
    mydb = mysql.connector.connect(user='root',host='localhost',passwd='rutuja',auth_plugin='mysql_native_password',database='recruitment_bot')
    mycursor = mydb.cursor() 

    # if mydb.is_connected():
    #     print("QuestionHistory")
    # else:
    #     print("fail")

    sql = 'insert into q_history (cand_id,qid,level,sim,concept) values ("{0}","{1}","{2}","{3}","{4}");'.format(cand_id,qid,level,sim,concept)
    mycursor.execute(sql) 
    mydb.commit()

def RetrieveQuestion(cand_id):
    mydb = mysql.connector.connect(user='root',host='localhost',passwd='rutuja',auth_plugin='mysql_native_password',database='recruitment_bot')
    mycursor = mydb.cursor() 
    
    # if mydb.is_connected():
    #     print("RetrieveQuestion")
    # else:
    #     print("fail")

    sql = 'select * from q_history where cand_id="{0}" order by id desc limit 1;'.format(cand_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchone()

    flag=1
    q_asked=[]
    if myresult== None:
        level=2
        sql = 'select * from dbms where Level="{0}";'.format(level)
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        q=random.choice(myresult)
        return(q)
    else:
        sql = 'select * from q_history where cand_id="{0}" order by id desc limit 1;'.format(cand_id)
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
        level = myresult[2]

        # list of questions already asked and concepts

        sql = 'select qid,concept from q_history where cand_id="{0}";'.format(cand_id)
        mycursor.execute(sql)
        res = mycursor.fetchall()
        q_asked = []
        concept_covered = []
        for i in res:
            q_asked.append(i[0])
            concept_covered.append(i[1])

        # no of questions asked from a current level
        sql = 'select count(qid) from q_history where cand_id="{0}" and level="{1}";'.format(cand_id,level)
        mycursor.execute(sql)
        count1 = mycursor.fetchall()
        count = count1[0][0]

        # average similarity for questions from current level 
        sql = 'select avg(sim) from q_history where cand_id="{0}" and level="{1}";'.format(cand_id,level)
        mycursor.execute(sql)
        sim = mycursor.fetchall()
        avg_sim = sim[0][0]


        # next Question
        if level==2:
            if count<2 or (avg_sim>=0.4 and avg_sim<0.6):
                level=2
            elif avg_sim>=0.6:
                level=3
            else:
                level=1
        elif level==3:
            if count<2 or (avg_sim>=0.6 and avg_sim<0.8):
                level=3
            elif avg_sim>=0.8:
                level=4
            else:
                level=2
        elif level==1:
            if count<2 or (avg_sim>=0.4 and avg_sim<0.5):
                level=1
            elif avg_sim>=0.5:
                level=2
            else:
                flag=0
        elif level==4:
            level=4

        if flag==1:
            if len(q_asked)==1:
                sql = 'select * from dbms where Level="{0}" and qid != {1} and concepts != "{2}";'.format(level,res[0][0],res[0][1])
            else:
                sql = 'select * from dbms where Level="{0}" and qid not in {1} and concepts not in {2};'.format(level,tuple(q_asked),tuple(concept_covered))
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            # if all concepts are covered from a particular level ask random question from that level
            if len(myresult) == 0:
                sql = 'select * from dbms where Level="{0}" and qid not in {1};'.format(level,tuple(q_asked))
                mycursor.execute(sql)
                myresult = mycursor.fetchall()

            # choose random question from list
            q=random.choice(myresult)
        else:
            q=(1,'stop')
        # print(q)
        return (q)


def UpdateSimilarity(sim,cand_id):
    mydb = mysql.connector.connect(user='root',host='localhost',passwd='rutuja',auth_plugin='mysql_native_password',database='recruitment_bot')
    mycursor = mydb.cursor() 

    # if mydb.is_connected():
    #     print("UpdateSimilarity")
    # else:
    #     print("fail")

    # fetching latest question entry
    sql = 'select max(id) from q_history where cand_id="{0}";'.format(cand_id)
    mycursor.execute(sql)
    id1 = mycursor.fetchall()
    latest_id = id1[0][0]
    # print(latest_id)

    # updating the similarity for latest question 
    sql='update q_history set sim="{0}" where cand_id="{1}" and id="{2}";'.format(sim, cand_id, latest_id)
    mycursor.execute(sql) 
    mydb.commit()



if __name__=="__main__":
    # cid=DataUpdate("Nidhi","900458795","Dedhai","IT",9.35,"nid@gmail.com","C")
    # print(cid)
    RetrieveQuestion(63)
    # UpdateSimilarity(0.8,56)
