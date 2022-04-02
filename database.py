import pymysql

class Database():
    def __init__(self):
        #link mysql database
        self.db = pymysql.connect(host='localhost',user='testuser',password='Aa123456',database='comp7640')
        self.database = self.db.cursor()

    def show(self,Table,Select,*Where):
        # SQL query
        if any(Where):
            where = Where[0]
            sql = f"SELECT {Select} FROM {Table} WHERE {where}"
        else:
            sql = f"SELECT {Select} FROM {Table}"
        try:
            self.database.execute(sql)
            #get query result
            results = self.database.fetchall()
            return list(results)
        except:
            print ("Error: unable to fetch data")
        self.db.close()

    def add(self,Table,Attribute,Value,mutiadd=False,date=False):
        # SQL insert
        if mutiadd:
            #mutinsert
            mutisql = []
            for i in Value:
                value = str(i).strip('[]')
                sql = f"INSERT INTO {Table}({Attribute}) VALUES ({value})"
                mutisql.append(sql)
            try:
                for j in mutisql:
                    self.database.execute(j)
                self.db.commit()
            except:
                self.db.rollback()
        else:
            #singleinsert
            value = str(Value).strip('[]')
            value = value.replace('\'NULL\'','NULL')
            if date:
                sql = f"INSERT INTO {Table}({Attribute}) VALUES ({value}, curdate())"
            else:
                sql = f"INSERT INTO {Table}({Attribute}) VALUES ({value})"
            try:
                self.database.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
        self.db.close()

    def delete(self,Table,Where,mutidel = False):
        # SQL delete
        if mutidel:
            #mutideletion
            mutisql = []
            for i in range(len(Where)):
                sql = f"DELETE FROM {Table} WHERE {Where[i]}"
                mutisql.append(sql)
            try:
                for j in mutisql:
                    self.database.execute(j)
                self.db.commit()
            except:
                self.db.rollback()
        else:
            #singledeletion
            sql = f"DELETE FROM {Table} WHERE {Where}"
            try:
                self.database.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
        self.db.close()

    def update(self,Table,Set,Where,mutiupdate=False):
        # SQL update
        if mutiupdate:
            #mutiupdate
            mutisql = []
            for i in range(len(Set)):
                sql = f"UPDATE {Table} SET {Set[i]} WHERE {Where[i]}"
                mutisql.append(sql)
            try:
                for j in mutisql:
                    self.database.execute(j)
                self.db.commit()
            except:
                self.db.rollback()
        else:
            #singleupdate
            sql = f"UPDATE {Table} SET {Set} WHERE {Where}"
            try:
                self.database.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
        self.db.close()      