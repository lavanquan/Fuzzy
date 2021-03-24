import numpy as np
import math
from scipy.spatial import distance

import Parameter as para


def to_string(node):
    """
    print information of a node
    :param node: sensor node
    :return: None
    """
    print("Id =", node.id, "Location =", node.location, "Energy =", node.energy, "ave_e =", node.avg_energy,
          "Neighbor =", node.neighbor)


# def find_receiver(node, net):
#     """
#     find receiver node
#     :param node: node send this package
#     :param net: network
#     :return: find node nearest base from neighbor of the node and return id of it
#     """
#     if not node.is_active:
#         return -1
#     list_d = [distance.euclidean(para.base, net.node[neighbor_id].location) if net.node[
#         neighbor_id].is_active else float("inf") for neighbor_id in node.neighbor]
#     id_min = np.argmin(list_d)
#     if distance.euclidean(node.location, para.base) <= list_d[id_min]:
#         return -1
#     else:
#         return node.neighbor[id_min]

def calculate_angle(node):
    x, y = node.location
    x_base, y_base = para.base
    X = x - x_base
    Y = y - y_base
    return math.acos(X/math.sqrt(X**2 + Y**2)) 

def find_receiver(node, net):
    """
    find receiver node
    :param node: node send this package
    :param net: network
    :return: find node nearest base from neighbor of the node and return id of it
    """
    if not node.is_active:
        return -1
    candidate = [neighbor_id for neighbor_id in node.neighbor if
                 net.node[neighbor_id].level < node.level and net.node[neighbor_id].is_active]
    if candidate:
        d = [distance.euclidean(net.node[candidate_id].location, para.base) for candidate_id in candidate]
        id_min = np.argmin(d)
        return candidate[id_min]
    else:
        return -1


def request_function(node, mc, t):
    """
    add a message to request list of mc.
    :param node: the node request
    :param mc: mobile charger
    :param t: time get request
    :return: None
    """
    mc.request_list.append(node)


def estimate_average_energy(node):
    """
    function to estimate average energy
    user can replace with other function
    :return: a scalar which is calculated from check point list
    """
    return node.check_point[-1]["avg_e"]
