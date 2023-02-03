'''
Elasticsearch 操作模块

NOTE: 
    Elasticsearch库是有版本兼容性的。
        6.x 只能用于 6.x 的ES服务器，同样，API 也可能不一样。

    ESapi.py 的意义在于，向上层封装统一接口，以应对服务器API的变动。

'''
import time
import uuid
import logging
import datetime
from elasticsearch import Elasticsearch

class Base: 
    ''' ES 基础类 '''
    def __init__(
        self, url:list=None) -> None:
        ''' 
        初始化 ES 基础类 
        
        Example:
            url=['http://user:password@localhost:9200']
        
        '''
        self.client = Elasticsearch(url)

    def Base_IndexList(self, index=None): 
        ''' 
        返回索引列表 
        
        Args:
            index:      索引名，可用通配符。
        
        Returns: 
            [{
                'health': 'green', 
                'status': 'open', 
                'index': 'serverlog-2022.11.28', 
                'uuid': 'egiGnmdhQ3i6Aa6-FlseKA', 
                'pri': '1', 
                'rep': '1', 
                'docs.count': '603343', 
                'docs.deleted': '0', 
                'store.size': '574.9mb', 
                'pri.store.size': '287.4mb'}]

        '''
        data = self.client.cat.indices(format='json')
        return data

    def Base_CreateIndex(self, index_name:str, index_setting:dict): 
        ''' 
        创建索引 
        
        Args: 
            index_name:     索引名
            index_setting:  索引配置

        Returns: 返回ES的信息
            {
                '_index': 'itsm_user_log', 
                '_type': '_doc', 
                '_id': 'DhesFYYBBzWsfIngUNzR', 
                '_version': 1, 
                'result': 'created', 
                '_shards': {
                    'total': 2, 
                    'successful': 1, 
                    'failed': 0}, 
                '_seq_no': 10, 
                '_primary_term': 1}
        '''
        data = self.client.index(index=index_name, body=index_setting)
        return data

    def Base_DeleteIndex(self, index_name:str): 
        ''' 
        删除指定索引 
        
        删除成功返回 True
        '''
        if self.client.indices.exists(index_name):
            d = self.client.indices.delete(index_name)
            if d.get('acknowledged'): 
                return True
            return False
        else: 
            logging.warn('要删除的索引不存在。 index: %s', index_name)
            return False


# 示例
class AppLog(Base): 
    ''' 
    用户日志类 
    
    Example: 
    ```
    # Init
    IU = ItsmUserLog(['http://user:password@localhost:9200'])
    # Create Index
    IU.Base_CreateIndex('your_index', IU.INDEX_SETTING)     
    # Insert Data
    IU.Add('ttst','INFO','test data')
    # Query
    IU.FullQuery('keys keys')
    ```
    
    '''
    INDEX_SETTING = {
        'mappings':{
            'level': {'type': 'keyword'}, 
            'message': {'type': 'text'}, 
            'logtime': {'type': 'date', 'format': 'yyyy-MM-dd HH:mm:ss'}
        }
    }

    def __init__(self, url: list = None) -> None:
        super().__init__(url)

    def Add(self, level:str=None,
        message:str=None, logtime:datetime=datetime.datetime.now()):
        ''' 
        插入数据
        
        Returns: 插入成功返回 True
        '''
        try: 
            d = self.client.create(
                'app_log',
                id=str(time.time()) + str(uuid.uuid4()), 
                body={
                    "logtime": logtime, 
                    "level": level, 
                    "message": message, 
                }
            )
            if d.get('result') == 'created': 
                return True
            else: 
                return False
        except Exception as e: 
            logging.error('插入日志到 ES 时发生异常，%s', str(e))
            return False
    
    def FullQuery(self, keys=None, level=None, 
        size=100, page=1, sort=True, nosysinfo=True):
        ''' 
        搜索内容 

        Args:
            keys:       搜索关键词，（空格分词）
            size:       结果页大小
            page:       页码
            nosysinfo:  不返回系统字段，直接返回数据字段
        
        Returns:
            [{}]
        '''
        body = {
            'from': page, 
            'size': size,
            'query': {
                'bool': {
                    'must': []
                }
            }
        }
        # 条件
        if keys is not None: 
            body['query']['bool']['must'].append({
                'multi_match': {'query': keys}
            })
        if level is not None: 
            body['query']['bool']['must'].append({ 
                'match': {
                    'level': {'query': level, 'boost': 2 } 
                }
            })
        if sort: 
            body['sort'] = {'logtime': {'order': 'desc'} }
        # 查询
        data = self.client.search(index='app_log', body=body)
        # 判断数据
        if data['_shards']['failed'] != 0: 
            logging.warning(
                '查询ES时，出现失败的分片。数量：%s', 
                str(data['_shards']['failed']))
        # 输出
        if nosysinfo: 
            redata = []
            for i in data['hits']['hits']: 
                redata.append(i.get('_source'))
            return redata
        else:
            return data
    