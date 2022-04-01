import pymysql

class Database():
    def __init__(self):
        #link mysql database
        self.db = pymysql.connect(host='localhost',user='testuser',password='test123',database='TESTDB')
        self.database = self.db.cursor()

    def show(self,Table,Select,*Where):
        # SQL 查询语句
        # table = Table
        # select = Select
        # where = Where
        if any(Where):
            where = Where[0]
            sql = f"SELECT {Select} FROM {Table} WHERE {where}"
        else:
            sql = f"SELECT {Select} FROM {Table}"
        try:
            # 执行SQL语句
            self.database.execute(sql)
            # 获取所有记录列表
            results = self.database.fetchall()
            return list(results)
        except:
            print ("Error: unable to fetch data")
        
        self.db.close()

    def add(self,Table,Attribute,Value,mutiadd=False,date=False):
        # SQL 插入语句
        # table = Table
        # attribute = Attribute
        if mutiadd:
            #mutiadd
            #Value = [['i15', 'apple', 40], ['i16', 'banana', 50]]
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
                # 如果发生错误则回滚
                self.db.rollback()
        else:
            #singleadd
            value = str(Value).strip('[]')
            if date:
                sql = f"INSERT INTO {Table}({Attribute}) VALUES ({value}, curdate())"
            else:
                sql = f"INSERT INTO {Table}({Attribute}) VALUES ({value})"
            try:
                # 执行sql语句
                self.database.execute(sql)
                # 提交到数据库执行
                self.db.commit()
            except:
                # 如果发生错误则回滚
                self.db.rollback()
        
        self.db.close()

    def delete(self,Table,Where,mutidel = False):
        # SQL 删除语句
        if mutidel:
            mutisql = []
            for i in range(len(Where)):
                sql = f"DELETE FROM {Table} WHERE {Where[i]}"
                mutisql.append(sql)
            try:
                for j in mutisql:
                    self.database.execute(j)
                self.db.commit()
            except:
                # 如果发生错误则回滚
                self.db.rollback()
        else:
            sql = f"DELETE FROM {Table} WHERE {Where}"
            try:
                # 执行SQL语句
                self.database.execute(sql)
                # 提交到数据库执行
                self.db.commit()
            except:
                # 发生错误时回滚
                self.db.rollback()
        # 关闭连接
        self.db.close()

    def update(self,Table,Set,Where,mutiupdate=False):
        # SQL 更新语句
        # table = Table
        # where = Where
        if mutiupdate:
            mutisql = []
            for i in range(len(Set)):
                sql = f"UPDATE {Table} SET {Set[i]} WHERE {Where[i]}"
                mutisql.append(sql)
            try:
                for j in mutisql:
                    self.database.execute(j)
                self.db.commit()
            except:
                # 如果发生错误则回滚
                self.db.rollback()
        else:
            sql = f"UPDATE {Table} SET {Set} WHERE {Where}"
            try:
                # 执行SQL语句
                self.database.execute(sql)
                # 提交到数据库执行
                self.db.commit()
            except:
                # 发生错误时回滚
                self.db.rollback()
        
        # 关闭数据库连接
        self.db.close()      