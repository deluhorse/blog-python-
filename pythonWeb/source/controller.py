# -*- coding:utf-8 -*-

import importlib
import sys

import requests
import tornado.escape
import tornado.gen
import tornado.ioloop
import tornado.web


class Controller(tornado.web.RequestHandler):
    """ 
    基类
    """

    controllerKey = ''  # controller对应的key
    user_type = ''  # controller对应的用户权限 buyer买家可以调用 seller商家可以调用 admin管理员可以调用 为空则无权限控制
    config = None
    view_data = {}  # 模板输出数据
    model = None
    _GET = False
    _POST = False
    requests = requests
    view_path = ''
    escape = tornado.escape

    def initialize(self):
        """
        初始化
        :return: 
        """
        self.view_path = self.config['VIEW_PATH']

    def on_finish(self):
        """
        """
        # self.model.__del__()

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """ 接受GET请求
            固定参数a，如果a有值，调用同名方法，如果a没有值，调用index方法
        """

        action = self.params('a')
        action = action if action else 'index'

        # 请求类型
        self._GET = True

        if action:
            if not self.config['debug']:
                try:
                    method = eval('self.' + action)
                    method()
                except Exception, e:
                    print e
                    self.redirect('/error')
            else:
                method = eval('self.' + action)
                method()

        return

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """ 
        接受POST请求
        固定参数a，如果a有值，调用同名方法，如果a没有值，调用index方法
        """

        action = self.params('a')
        action = action if action else 'index'

        # 请求类型
        self._POST = True

        if action:
            if not self.config['debug']:
                try:
                    method = eval('self.' + action)
                    method()
                except Exception, e:
                    print e
                    self.redirect('/error')
            else:
                method = eval('self.' + action)
                method()
        return

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def request(self, url, request_type, data):
        """ 
        发起请求

        @params url string 请求地址
        @params type string 请求类型，可以是GET，POST
        @params data dict 发送数据
        """

        if request_type == 'POST':
            res = self.requests.post(url, data)
            return res.text

        if request_type == 'GET':
            res = self.requests.get(url, data)
            return res.text

        return 'type error, must POST or GET'

    @tornado.gen.coroutine
    def display(self, view_name, view_path=''):
        """ 
        输出模板
        调用模板输出，使用当前类名为模板目录
        @params viewName string 调用模板名称
        @params data dict 输出数据
        """

        view_path = view_path if view_path else self.view_path

        if not self.config['debug']:
            try:
                self.render("%s/%s/%s.html" % (view_path, self.__class__.__name__, view_name),
                            controller=self.__class__.__name__, **self.view_data)
            except Exception, e:
                print e
                self.redirect('/700')
                return
        else:
            self.render("%s/%s/%s.html" % (view_path, self.__class__.__name__, view_name),
                        controller=self.__class__.__name__, **self.view_data)

    def params(self, key, data_type=None):
        """ 
        获取请求参数
        如果只有一个值，将其转为字符串，如果是list，保留list类型
        @:param key 参数名称
        @:param data_type 返回数据类型，默认
        """

        try:
            value = self.request.arguments[key]
            if len(value) > 1:
                value_strip = []
                for item in value:
                    value_strip.append(item.strip())
                return value_strip
            else:
                return value[0].strip()
        except Exception, e:
            print e
            return ''

    def import_model(self, model_name):
        """ 
        加载类
        @:param model_name 类名
        @:param model_dir 目录
        """

        try:
            model = importlib.import_module(self.version + '.model.' + model_name)
            return model.Model(self.model)
        except Exception, e:
            print e
            return None

    def import_service(self, service_name):
        """ 
        加载服务类
        @params service_name 服务类名
        @params service_dir 服务类所在目录
        """

        try:
            service = importlib.import_module(self.version + '.service.' + service_name)
            return service.Service()
        except Exception, e:
            print e
            return None


class server(object):
    """ 启用服务
    """

    def start(self, route, setting):

        # 获取参数
        argv = sys.argv
        if len(argv) < 2:
            print 'no port, eg. python2 index.py 9000'
            exit()

        host = argv[1]
        hosts = host.split(':')
        if len(hosts) == 2:
            host = hosts[0]
            port = hosts[1]
        else:
            host = '0.0.0.0'
            port = hosts[0]

        app = tornado.web.Application(route, **setting)
        app.listen(port, address=host)
        tornado.ioloop.IOLoop.instance().start()

# class error(Controller):
#   """ 错误处理
#   """
#
#   def index(self):
#       self.display('404', '../view')
