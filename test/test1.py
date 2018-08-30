# -*- coding:utf-8 -*-

"""
@author: delu
@file: test1.py
@time: 18/5/24 16:59
要求从m个数种取n个数，这n个数的和尽量大且不能超过x
思路说明:
先排序，去最小的n个数组成array_a
剩下的数组成b
"""
# 找到两个数尽可能接近8，但是小于8
array_a = [1, 2, 3, 4]
x = 8
nums = 2
# 排序
array_a.sort()
array_b = array_a[nums:]
array_a = array_a[:nums]
print array_a
print array_b

#


