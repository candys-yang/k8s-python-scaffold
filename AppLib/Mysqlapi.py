'''
Mysql 操作模块

NOTE: 
    Mysql 操作的函数超过 20个，应将 ORM 和 查询 单独放一个 .py 


'''
import datetime
import logging
from sqlalchemy import create_engine
from sqlalchemy import Column, Date, ForeignKey, String, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import INTEGER,VARCHAR
from sqlalchemy.orm import sessionmaker


class Base: 
    ''' Mysql基础类 '''
    def __init__(self, mysqlurl) -> None:
        self.engine = create_engine(mysqlurl)
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.session = self.sessionmaker()

    def _QueryResultToDict(self, row, strftime = None): 
        ''' 查询结果转换为字典 '''
        rows = []
        if row == [None]: return rows
        for i in row:
            _i = i.__dict__
            del _i['_sa_instance_state']
            if strftime: 
                for ii in _i:
                    if type(_i[ii]) == datetime.date: 
                        _i[ii] = _i[ii].strftime(strftime)
                    if type(_i[ii]) == datetime.datetime:
                        _i[ii] = _i[ii].strftime(strftime)
            rows.append(_i)
        return rows

    def CheckMysql(self): 
        '''
        检查数据库可用性。 
        '''  
        try:
            conn = self.engine.connect()
            logging.info('Check Mysql Connect: Success')
            for i in conn.execute('show global status;').fetchall(): 
                if i[0] in [
                    'Memory_used', 'Open_files', 'Open_tables', 
                    'Qcache_total_blocks', 'Uptime', 
                    'Threads_running', 'Innodb_page_size']:
                    logging.info('Mysql Status: ' + str(i))
            conn.close()
        except Exception as e: 
            logging.error('检查数据库连接时发生错误: ' + str(e))

'''
Example:

    class sqlorm: 
        class User(Base):
            __tablename__ = 'user'
            id = Column(INTEGER(11), primary_key=True)
            username = Column(String(50))
            password = Column(String(254))

    class Test(Base): 
        def __init__(self, mysqlurl) -> None: 
            super().__init__(mysqlurl)
        
        def GetUser(self): 
            Table = sqlorm.User
            tj = set()
            tj.add(Table.id != 0)
            row = self.session.query(Table).filter(*tj).all()
            self.session.close()
            return self._QueryResultToDict(row)
'''