import tornado.ioloop
import tornado.web
import tornado.options
import json, random
from PIL import Image
from io import BytesIO
import os
import logging, traceback as tk
import keras.backend
from keras.models import model_from_json
from model import *


Model = TrainCNNModel()
Model.build()

Model.reload_model()
Model.model.summary()
print(Model.model.evaluate(sequence_test_data , verbose=1))


 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
 
    def post(self):
        
        img = Image.open(BytesIO(self.request.files['image'][0]['body']))
   
        data = Model.orc_img(img)
        self.write(json.dumps(
            {"code": 200, "data": data
             }))


def make_app():
    template_path = "templates/"
    static_path = "./static/"

    return tornado.web.Application([

        (r"/", MainHandler),

    ], template_path=template_path, static_path=static_path, debug=True)


def run_server(port=8000):
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(port)
    print("\n服务已启动 请打开 http://127.0.0.1:8000 ")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run_server()
