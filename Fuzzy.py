import numpy as np
import math

from scipy.spatial.distance import euclidean
import Parameter as para
from Fuzzy_method import check_request, self_charge
from Fuzzy_FLCSD import estimate
class Fuzzy:
    def __init__(self):
        pass
    
    def update(self, mc, network, time_stem, check_func=check_request, self_charge_func=self_charge):
        ECR_max = network.get_max_ECR()
        D_max = network.get_max_D()
        CN_max = network.get_max_CN()
        checked_request_list = check_func(mc)
        if len(checked_request_list) == 0:
            print("MC#{}: self charge".format(mc.id))
            return self_charge_func(mc)
        pos = (0, 0)
        time = 0
        max_estimate = -1
        choosen_index = -1
        for index, node in enumerate(checked_request_list):
            node_estimate = estimate(node.energy, node.energy_max, euclidean(node.location, mc.current), D_max, node.critical_density, CN_max, node.avg_energy, ECR_max)
            if node_estimate > max_estimate:
                pos = node.location
                time = (node.energy_max - node.energy)/(para.alpha / (para.beta ** 2))
                choosen_index = index
                max_estimate = node_estimate
        # print("MC#{}: charge at {} for {}s".format(mc.id, pos, time))
        node = checked_request_list[choosen_index]
        # print("choosen node: e={} max_e={} d={} dmax={} CN={} CN_max={} avg={} max_avg={}".format(node.energy, node.energy_max, euclidean(node.location, mc.current), D_max, node.critical_density, CN_max, node.avg_energy, ECR_max))
        return pos, time
        

