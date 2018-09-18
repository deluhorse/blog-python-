# -*- coding:utf-8 -*-

"""
@author: delu
@file: red_black_tree.py
@time: 18/9/12 14:33
"""

BLACK = 'black'
RED = 'red'

node = {
    'color': RED,
    'value': '',
    'left_child': None,
    'right_child': None,
    'parent': None
}


# class RedBlackTree():
#     root_node = None
#
#     current_height = 0
#
#     def insert(self, node):
#         """
#         默认插入黑节点，需要变色和旋转的额外处理
#         :param node:
#         :return:
#         """
#         if not self.root_node:
#             # 如果树为空，则当前节点为根节点, 并设置节点颜色为黑
#             node['color'] = BLACK
#
#             self.root_node = node
#
#             self.current_height += 1
#
#         else:
#
#             parent_node, direction = self.find_parent_node(node, self.root_node)
#
#             if parent_node['color'] == BLACK:
#                 # 父节点是黑的，那么直接插入当前红节点，并且高度不变
#                 parent_node[direction] = node
#             elif parent_node['color'] == RED:
#                 # 父节点是红的，则当前节点必须为黑节点，此时整体高度变为1，需要进行旋转变换和变色操作
#
#
#     def find_insert_node(self, node, parent_node):
#         """
#         从根节点开始寻找能够插入的父节点
#         :param node:
#         :return:
#         """
#
#         if node['value']
