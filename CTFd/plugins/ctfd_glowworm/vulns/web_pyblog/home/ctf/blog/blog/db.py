import os
import sys
import psycopg2



def updateOperate():
    with open('/flag','r') as f:
        conn = psycopg2.connect(database="blog", user="blog", password="blog", host="127.0.0.1", port="5432")
        cursor=conn.cursor()
        cursor.execute("update auth_user set first_name='{}' where username='blog'".format(f.read()))
        conn.commit()
        print "Total number of rows updated :", cursor.rowcount

        cursor.execute("select username,first_name from auth_user")
        rows=cursor.fetchall()
        for row in rows:
            print 'username=',row[0], ',flag=',row[1],'\n'
        conn.close()
    
if __name__=='__main__':
    updateOperate()