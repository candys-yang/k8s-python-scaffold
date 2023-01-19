import redis 

con = redis.ConnectionPool()
con.from_url('redis://192.168.0.127:6379')
rc = redis.Redis(connection_pool=con,decode_responses=True)
print( rc.info("memory")['used_memory'] )