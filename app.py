''' Flask 应用脚手架 '''
import uuid
import logging
from flask import Flask, g, request

from AppLib import AppTypes, Mysqlapi, Redisapi
from Routes import *

#日志格式
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - [appname:%(filename)s:%(lineno)d]" + 
        " - %(levelname)s: %(message)s"
)

app = Flask(__name__)

# 消息中间件
@app.before_request
def before():
    reqhead = request.headers

    pass

@app.errorhandler(404)
@app.errorhandler(405)
def page4xx(e): 
    re = AppTypes.Response.Json(
        AppTypes.Status.NOFOUND, 
        "URL地址错误", 
        {}, 
        uuid.uuid4()
    )
    logging.warning("请求地址异常，" + str(e))
    return re.Dict()

@app.errorhandler(500)
def page5xx(e): 
    re = AppTypes.Response.Json(
        AppTypes.Status.ERROR, 
        "服务器内部错误",
        {}, 
        uuid.uuid4()
    )
    logging.error("未知的服务器错误，" + str(e))


# 路由规则
ROUTE_RULE = [
    ('/', index.Index)
]




if __name__ == '__main__': 
    # 应用配置
    app.config['JSON_AS_ASCII'] = False     #避免json中文乱码
    app.debug = True
    app.name = 'test'
    #
    for i in ROUTE_RULE:
        logging.info("Add Url Rule: " + str(i))
        app.add_url_rule(i[0], view_func=i[1].as_view(i[0]))

    # 日志
    #   屏蔽框架层面的INFO日志
    logging.getLogger("werkzeug").setLevel(logging.WARNING)     

    # 启动检查
    #   数据可可用性
    Mysqlapi.Base(
        Redisapi.Client('redis://127.0.0.1/0').redisc.get(
            'appname:MYSQL_MASTER'
        ).decode('utf-8')
    ).CheckMysql()
    

    # 运行服务
    app.run(host='0.0.0.0',port=5000)
    