'''
    定义应用的数据格式。


    python 是弱类型语言，开发过程中，应当对数据做标准化的约束。

    避免在日后维护中对数据对象产生疑惑。


'''

import enum


class Request:
    ''' 接口请求数据的数据映射 '''
    class Base:
        ''' 
        基本请求数据结构 
        
        请求的Json数据格式要求为： {token:, reqid:, params:{...}}

        Sample:

            req = AppTypes.Request.Base( request.get_json() )    \n
            print(req.params)

        '''
        def __init__(self, reqjson) -> None:
            self.token = None
            self.params = None
            self.reqid = None

            if 'token' in reqjson: 
                self.token = reqjson['token']
            if 'params' in reqjson:
                self.params = reqjson['params']
            if 'reqid' in reqjson: 
                self.reqid = reqjson['reqid']
            

class Status(enum.Enum):
    ''' 
    状态返回码 
    
    >>> ENUM: 
        SUCCESS = 200 
        BAD = -400 
        UNAUTH = -401
        NOACCESS = -403
        NOFOUND = -404
        FAILED = -413
        ERROR = -500
        TIMEOUT = -504
    '''
    SUCCESS = 200
    BAD = -400
    UNAUTH = -401
    NOACCESS = -403
    NOFOUND = -404
    FAILED = -413
    ERROR = -500
    TIMEOUT = -504


class Response:

    class Json:
        ''' 生成统一的 Response 返回对象 '''
        def __init__(self, status:Status, msg, result, reqid=None) -> None:
            self.status = status
            self.message = msg
            self.results = result
            self.reqid = reqid
            #
        def Dict(self): 
            ''' 返回 Dict 类型的数据 '''
            _re_results = None
            if type(self.results) == dict: 
                _re_results = self.results
            else:
                _re_results = self.results.__dict__
            return {
                "status": self.status.value,
                "message": self.message,
                "results": _re_results,
                "reqid": self.reqid
            }
        
        def Str(self) -> str:
            ''' 返回 Str 类型的数据 '''
            _re_results = None
            if type(self.results) == dict: 
                _re_results = self.results
            else:
                _re_results = self.results.__dict__

            return str({
                "status": self.status.value,
                "message": self.message,
                "results": _re_results,
                "reqid": self.reqid
            })






