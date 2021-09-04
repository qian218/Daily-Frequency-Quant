# Copyright (c) 2021 Dai HBG

"""
该代码定义的类用于计算一个信号的平均IC等统计值
This code is used for calculating the average IC and other statistical values of a signal

v1.0
2021-08-30
-- 定义：计算平均IC，信号自相关系数，IC_IR，IC为正的频率
"""

import numpy as np


class Stats:
    def __init__(self):
        self.ICs = []
        self.mean_IC = 0
        self.auto_corr = 0
        self.IC_IR = 0
        self.positive_IC_rate = 0


class AutoTester:
    def __init__(self):
        pass

    @staticmethod
    def test(signal, ret, top=None):
        """
        :param signal: 信号矩阵
        :param ret: 和信号矩阵形状一致的收益率矩阵，意味着同一个时间维度已经做了delay
        :param top: 每个时间截面上进入截面的股票位置
        :return: 返回Stats类的实例
        """
        signal[np.isnan(signal)] = 0
        if top is None:
            top = signal != 0
        ics = []
        auto_corr = []
        assert len(signal) == len(ret)
        assert len(signal) == len(top)
        for i in range(len(signal)):
            ics.append(np.corrcoef(signal[i, top[i]], ret[i, top[i]])[0, 1])
            if i >= 1:
                auto_corr.append(
                    np.corrcoef(signal[i, top[i] & top[i - 1]], ret[i, top[i] & top[i - 1]])[0, 1])

        ics = np.array(ics)
        ics[np.isnan(ics)] = 0
        auto_corr = np.array(auto_corr)
        auto_corr[np.isnan(auto_corr)] = 0

        stats = Stats()
        stats.ICs = ics
        stats.mean_IC = np.mean(ics)
        stats.auto_corr = np.mean(auto_corr)
        if len(ics) > 1:
            stats.IC_IR = np.mean(ics) / np.std(ics)
        stats.positive_IC_rate = np.sum(ics > 0) / len(ics)
        return stats
