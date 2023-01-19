import time
from flask.views import MethodView
from AppLib import AppTypes

class Index(MethodView): 
    def __init__(self) -> None:
        super().__init__()
        self.re = AppTypes.Response.Json(
            AppTypes.Status.SUCCESS,
            "欢迎访问首页", 
            {"date": time.time()}
        )

    def get(self): 
        return self.re.Dict()

    def post(self):
        return self.re.Dict()