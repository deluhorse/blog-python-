# -*- coding:utf-8 -*-

import MySQLdb
from DBUtils.PooledDB import PooledDB
from source.properties import properties


class ModelBase(object):
    """
    数据类
    """
    pool = PooledDB(
        creator=MySQLdb,
        mincached=5,
        maxcached=20,
        host=properties.get('jdbc', 'DB_HOST'),
        user=properties.get('jdbc', 'DB_USER'),
        passwd=properties.get('jdbc', 'DB_PASS'),
        db=properties.get('jdbc', 'DB_BASE'),
        port=int(properties.get('jdbc', 'DB_PORT')),
        use_unicode=1,
        charset='utf8'
    )

    def __init__(self):
        """ 
        初始化
        """
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    def find(self, str_table_name, str_type, dic_data, boo_format_data=True):
        """ 
        读取一组数据

        @params str_table_name string 表名
        @params str_type string 类型，可以是list, first
        @prams dic_data dict 数据字典
        @params booformat_data bool 是否格式化数据，默认为True
        """

        if boo_format_data:
            dic_data = self.format_data(dic_data)

        str_table_name = self.build_table_name(str_table_name)

        str_fields = self.build_fields(dic_data['fields'])

        str_condition = self.build_condition(dic_data['condition'])

        str_join = ''

        for join_item in dic_data['join']:
            str_join += self.build_join(join_item)

        str_limit = self.build_limit(dic_data['limit'])

        str_order = self.build_order(dic_data['order'])

        str_sql = "select %s from %s %s %s %s %s" % (
        str_fields, str_table_name, str_join, str_condition, str_order, str_limit)

        self.cursor.execute(str_sql)

        print str_sql

        if str_type == 'list':
            dic_list = self.cursor.fetchall()
        else:
            dic_list = self.cursor.fetchone()

        return dic_list

    def paginate(self, str_table_name, dic_data):
        """ 分页读取数据

        @params str_table_name string 表名
        @params dic_data dict 数据字典，可以包裹field, fields, condition等key
        """

        dic_data = self.format_data(dic_data)

        # 页码
        int_page = dic_data['page'] if dic_data.has_key('page') else 1
        int_page_num = dic_data['limit'][1] if dic_data.has_key('limit') else ''
        int_start_limit = (int_page - 1) * int(int_page_num)

        dic_data['limit'] = [str(int_start_limit), int_page_num]

        # 总条数
        int_rows = self.get_rows(str_table_name, {
            'fields': ['count(*) as count'],
            'condition': dic_data['condition'],
            'join': dic_data['join']
        }, False)

        # 获取数据
        tup_list = self.find(str_table_name, 'list', dic_data, False)

        return [tup_list, int_rows]

    def get_rows(self, str_table_name, dic_data, booformat_data=True):
        """ 获取数据记录数

        @params str_table_name string 表名
        @params dic_data dict 数据字典
        @params booformat_data bool 是否格式化数据，默认为True
        """

        if booformat_data:
            dic_data = self.format_data(dic_data)

        str_table_name = self.build_table_name(str_table_name)

        str_fields = self.build_fields(dic_data['fields'])

        str_join = ''

        for join_item in dic_data['join']:
            str_join.join(self.build_join(join_item))

        str_condition = self.build_condition(dic_data['condition'])

        str_sql = "select %s from %s %s %s" % (str_fields, str_table_name, str_join, str_condition)
        # print str_sql

        self.cursor.execute(str_sql)

        dic_rows = self.cursor.fetchone()

        return dic_rows['count'] if dic_rows else 0

    def insert(self, str_table_name, dic_data):
        """ 插入数据

        @params str_table_name string 表名
        @params dic_data dict 数据字典
        """
        res = -1
        str_sql = ''
        try:
            dic_data = self.format_data(dic_data)
            str_table_name = self.build_table_name(str_table_name)
            str_sql = "insert into %s (%s) values (%s)" % (str_table_name, dic_data['key'], dic_data['val'])

            res = self.cursor.execute(str_sql)
            self.conn.commit()
        except Exception, e:
           print str_sql
           print Exception, ':', e
        return res

    def update(self, str_table_name, dic_data):
        """ 修改数据

        @params str_table_name string 表名
        @params dic_data dict 数据字典
        """

        dic_data = self.format_data(dic_data)
        str_table_name = self.build_table_name(str_table_name)
        str_fields = self.build_fields(dic_data['fields'])
        str_condition = self.build_condition(dic_data['condition'])

        str_sql = "update %s set %s %s" % (str_table_name, str_fields, str_condition)

        print str_sql

        self.cursor.execute(str_sql)

        self.conn.commit()

    def delete(self, str_table_name, dic_data):
        """ 删除数据

        @params str_table_name string 表名
        @params dic_data dict 数据字典
        """

        dic_data = self.format_data(dic_data)
        str_table_name = self.build_table_name(str_table_name)
        str_condition = self.build_condition(dic_data['condition'])

        str_sql = "delete from %s %s" % (str_table_name, str_condition)

        print str_sql

        self.cursor.execute(str_sql)

        self.conn.commit()

    def format_data(self, dic_data):
        """ 格式化数据
        将fields, condition, join 等数据格式化返回

        @params dic_data dict 数据字典
        """

        # fileds
        dic_data['fields'] = dic_data['fields'] if dic_data.has_key('fields') else ''

        # join
        dic_data['join'] = dic_data['join'] if dic_data.has_key('join') else []

        # conditon
        dic_data['condition'] = dic_data['condition'] if dic_data.has_key('condition') else ''

        # order
        dic_data['order'] = dic_data['order'] if dic_data.has_key('order') else ''

        # limit
        dic_data['limit'] = dic_data['limit'] if dic_data.has_key('limit') else ''

        # key
        dic_data['key'] = dic_data['key'] if dic_data.has_key('key') else ''

        # val
        dic_data['val'] = dic_data['val'] if dic_data.has_key('val') else ''

        return dic_data

    def build_table_name(self, str_table_name):
        """ 构建表名
        根据配置文件中的表前辍，构建表名

        @params str_table_name string 表名
        """

        str_table_name = properties.get('jdbc', 'DB_TABLE_PRE') + str_table_name \
            if properties.get('jdbc', 'DB_TABLE_PRE') else str_table_name

        return str_table_name

    def build_fields(self, lisFields):
        """ 构建读取字段

        @params lisFields list 字段列表
        """

        str_fields = ','.join(lisFields) if lisFields else '*'

        return str_fields

    def build_join(self, str_join):
        """ 构建Join

        @params dicCondition dict 条件字典
        """

        return 'LEFT JOIN %s ON (%s)' % (str_join['table_name'] if str_join['table_name'] else '',
                                         str_join['join_condition'] if str_join['join_condition'] else '')

    def build_condition(self, str_condition):
        """ 构建条件

        @params dicCondition dict 条件字典
        """

        return 'where %s' % str_condition if str_condition else ''

    def build_order(self, str_order):
        """ 构建order
        未完成

        @params
        """

        # str_order = str_order

        return 'order by ' + str_order if str_order else ''

    def build_limit(self, lisLimit):
        """ 构建limit

        @params lisLimit list limit
        """

        str_limit = ','.join(lisLimit) if lisLimit else ''

        return 'limit ' + str_limit if str_limit else ''

    def escapeString(self, dic_data):
        if dic_data:
            if isinstance(dic_data, dict) == False:
                # print dic_data
                if type(dic_data) == str or type(dic_data) == unicode:
                    dic_data = dic_data.encode('utf8')
                return MySQLdb.escape_string(dic_data)
            else:
                for k, v in dic_data.iteritems():
                    # print type(v)
                    if type(v) == str or type(v) == unicode:
                        v = v.encode('utf8')
                    # print v

                    dic_data[k] = MySQLdb.escape_string(str(v))
                    # dic_data[k] = str(v).replace('\'', '\\\'').replace('"', '\"')
                # exit()
                return dic_data
        return False

    def __del__(self):

        self.cursor.close()
        self.conn.close()
        # self.db.close()
