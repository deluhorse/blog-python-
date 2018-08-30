# -*- coding:utf-8 -*-

"""
@author: delu
@file: meituan1.py
@time: 18/5/29 18:34
"""
import sys
a = sys.stdin.readline().split()
n = int(a[0])
m = int(a[1])
goods_array = []
full_cut_array = []
for i in range(n):
    # 输入商品金额预计是否允许特价优惠
    line = sys.stdin.readline().strip()
    # 把每一行的数字分隔后转化成int列表
    values = map(int, line.split())
    goods_array.append(values)
for i in range(m):
    # 输入满减活动优惠
    line = sys.stdin.readline().strip()
    # 把每一行的数字分隔后转化成int列表
    values = map(int, line.split())
    full_cut_array.append(values)
goods_total = 0
special_discount = 0
full_cut_discount = 0
discount_rate = 0.8
for goods in goods_array:
    # 遍历商品，如果存在物品有特价优惠，则不使用满减
    if goods[1] == 1:
        # 当前商品允许使用特价优惠
        special_discount += goods[0]
    goods_total += goods[0]
special_discount = special_discount * 0.8
for full_cut in full_cut_array:
    # 遍历满减活动，找出满减折扣最大的
    if goods_total >= full_cut[0] and full_cut[1] > full_cut_discount:
        full_cut_discount = full_cut[1]
if special_discount < goods_total - full_cut_discount:
    print float('%.03f' % special_discount)
else:
    print float('%0.3f' % goods_total - full_cut_discount)
