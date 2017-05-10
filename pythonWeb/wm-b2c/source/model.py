# -*- coding:utf-8 -*-

import MySQLdb
from DBUtils.PooledDB import PooledDB
from source.properties import properties
from source.sql_builder import SqlBuilder
from source.sql_constants import SqlConstants


class ModelBase(SqlBuilder):
    """
    数据类
    """
    sql_constants = SqlConstants
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

    def do_sqls(self, params_list):
        # 执行多条sql
        sql = ''
        try:
            for params in params_list:

                sql_type = params[self.sql_constants.SQL_TYPE]
                table_name = params[self.sql_constants.TABLE_NAME]
                dict_data = params[self.sql_constants.DICT_DATA]
                value_tuple = params[self.sql_constants.VALUE_TUPLE]

                if sql_type == self.sql_constants.INSERT:
                    #  创建
                    sql = self.build_insert(table_name, dict_data)
                elif sql_type == self.sql_constants.BATCH_INSERT:
                    # 批量创建
                    sql = self.build_batch_insert(table_name, dict_data)
                elif sql_type == self.sql_constants.UPDATE:
                    # 更新
                    sql = self.build_update(table_name, dict_data)
                elif sql_type == self.sql_constants.DELETE:
                    # 删除
                    sql = self.build_delete(table_name, dict_data)
                self.cursor.execute(sql, value_tuple)
            if params_list:
                self.conn.commit()
                return self.sql_constants.SUCCESS
        except Exception, e:
            self.conn.rollback()
            print Exception, ':', e
            print sql
            return None

    def page_find(self, table_name, params, value_tuple):
        """
        分页查询
        :param params: 
        :return: 
        """
        # 分页查询
        sql = self.build_paginate(table_name, params)
        sql_count = self.build_get_rows(table_name, params)
        try:
            self.cursor.execute(sql, value_tuple)
            dict_list = self.cursor.fetchall()

            self.cursor.execute(sql_count, value_tuple)
            dic_rows = self.cursor.fetchone()

            return [dict_list, dic_rows[self.sql_constants.ROW_COUNT] if dic_rows else 0]
        except Exception, e:
            print sql
            print sql_count
            print Exception, ':', e
            return None

    def get_rows(self, table_name, params, value_tuple):
        """
        统计数量
        :param params: 
        :return: 
        """
        sql_count = self.build_get_rows(table_name, params)
        try:
            self.cursor.execute(sql_count, value_tuple)
            dic_rows = self.cursor.fetchone()

            return dic_rows[self.sql_constants.ROW_COUNT] if dic_rows else 0
        except Exception, e:
            print sql_count
            print Exception, ':', e
            return 0

    def find(self, table_name, params={}, value_tuple=(), str_type='one' ):
        """
        查询
        :param params: 
        :return: 
        """
        sql = self.build_select(table_name, params)
        try:

            self.cursor.execute(sql, value_tuple)
            if str_type == self.sql_constants.LIST:
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchone()
        except Exception, e:
            print sql
            print Exception, ':', e
            return False

    def insert(self, table_name, params, value_tuple):
        """
        创建
        :param params: 
        :return: 
        """
        sql = self.build_insert(table_name, params)
        try:
            self.cursor.execute(sql, value_tuple)
            self.conn.commit()
            return self.sql_constants.SUCCESS
        except Exception, e:
            print sql
            print Exception, ':', e
            self.conn.rollback()
            return None

    def update(self, table_name, params, value_tuple):
        """
        更新
        :param params: 
        :return: 
        """
        sql = self.build_update(table_name, params)
        try:
            self.cursor.execute(sql, value_tuple)
            self.conn.commit()
            return self.sql_constants.SUCCESS
        except Exception, e:
            print sql
            print Exception, ':', e
            self.conn.rollback()
            return None

    def delete(self, table_name, params, value_tuple):
        """
        删除
        :param params: 
        :return: 
        """
        sql = self.build_delete(table_name, params)
        try:
            self.cursor.execute(sql, value_tuple)
            self.conn.commit()
            return self.sql_constants.SUCCESS
        except Exception, e:
            print sql
            print Exception, ':', e
            self.conn.rollback()
            return None

    def __del__(self):

        print 'close db'
        self.cursor.close()
        self.conn.close()
        # self.db.close()
