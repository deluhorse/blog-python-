# -*- coding:utf-8 -*-

from base import Base

# 错误处理
class Error(Base):

    def initialize(self):
        Base.initialize(self)

    def index(self):
        self.display('404')
