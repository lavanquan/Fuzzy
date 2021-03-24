import numpy as np
import math
import Parameter as para
from scipy.spatial.distance import euclidean

def check_request(mc):
    new_request_list = []
    for node in mc.request_list:
        time_move = (euclidean(mc.current, node.location) + euclidean(node.location, para.depot))/mc.velocity
        energy_consumption = time_move*mc.e_move
        if mc.energy > energy_consumption:
            new_request_list.append(node)
    return new_request_list

def self_charge(mc):
    pos = para.depot
    time_move = euclidean(mc.current, para.depot)/mc.velocity
    time_charge = (mc.capacity - (mc.energy - time_move*mc.e_move))/mc.e_self_charge
    return pos, time_charge