'''
    工厂函数
'''
import time
import logging
import redis


class RedisClient:
    ''' Redis 工厂函数 '''
    def __init__(self, url) -> None:
        ''' 初始化工厂函数对象 '''
        self.redis_url = url
        self.connection_pool = self._ConnectionPool()
        self.redisc = self.RedisClient()
        pass

    def _ConnectionPool(self): 
        ''' 创建连接池 '''
        return redis.ConnectionPool().from_url(self.redis_url)

    def _Ping(self, retest = True, count = 0):
        ''' 连接存活检查，一般使用默认参数调用即可，retest 是否在ping失败时重试。'''
        if count >= 3: raise "Connection Redis Failed"
        try:
            self.redisc.ping()
        except Exception as e:
            logging.error(str(e))
            time.sleep(3)
            _count = count + 1
            self._Ping(retest, _count)

    def RedisClient(self): 
        ''' 实例化一个 Redis 客户端，用于 Redis 操作 '''
        return redis.Redis(connection_pool= self.connection_pool, decode_responses=True)

class RedisOM:
    ''' Redis 对象映射 '''

    class RedisMemory:
        '''
        初始化 Redis 服务器的 Memory 数据映射对象
        
        Attributes:
            used_memory:            is redis command [info] the used_memory
            total_system_memory:    is redis command [info] the total_system_memory

        Example:

            RC = RedisClient('redis://127.0.0.1')   \n
            ROM = RedisOM.RedisMemory(RC)           \n
            print(ROM.total_system_memory)
        '''
        def __init__(self, rc:RedisClient) -> None:
            self._redisc = rc.RedisClient()
            self.used_memory = None
            self.total_system_memory = None
            self._GetLatest()

        def _GetLatest(self):
            memobj = self._redisc.info("memory")
            self.used_memory = memobj['used_memory']
            self.total_system_memory = memobj['total_system_memory']


