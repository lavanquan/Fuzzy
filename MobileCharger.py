from scipy.spatial import distance

import Parameter as para
from MobileCharger_Method import get_location, charging


class MobileCharger:
    def __init__(self, id,  energy=None, e_move=None, start=para.depot, end=para.depot, velocity=None,
                 e_self_charge=None, capacity=None):
        self.id = id
        self.is_stand = False  # is true if mc stand and charge
        self.is_self_charge = False  # is true if mc is charged
        self.is_active = False
        self.request_list = []

        self.start = start  # from location
        self.end = end  # to location
        self.current = start  # location now
        self.end_time = -1

        self.energy = energy  # energy now
        self.capacity = capacity  # capacity of mc
        self.e_move = e_move  # energy for moving
        self.e_self_charge = e_self_charge  # energy receive per second
        self.velocity = velocity  # velocity of mc

    def get_status(self):
        if not self.is_active:
            return "deactivated"
        if not self.is_stand:
            return "moving"
        if not self.is_self_charge:
            return "charging"
        return "self charging"

    def update_location(self, func=get_location):
        self.current = func(self)
        self.energy -= self.e_move

    def charge(self, net=None, func=charging):
        func(self, net)

    def self_charge(self):
        self.energy = min(self.energy + self.e_self_charge, self.capacity)

    def check_state(self):
        if distance.euclidean(self.current, self.end) < 1:
            self.is_stand = True
            self.current = self.end
        else:
            self.is_stand = False
        if distance.euclidean(para.depot, self.end) < 10 ** -3:
            self.is_self_charge = True
        else:
            self.is_self_charge = False

    def get_next_location(self, network, time_stem, optimizer=None):
        next_location, charging_time = optimizer.update(self, network, time_stem)
        self.start = self.current
        self.end = next_location
        moving_time = distance.euclidean(self.start, self.end) / self.velocity
        self.end_time = time_stem + moving_time + charging_time

    def run(self, network, time_stem, net=None, optimizer=None):
        if (self.end_time > time_stem):
            self.is_active = True
            if distance.euclidean(self.current, self.end) < 10**(-3):
                self.is_stand = True
                self.current = self.end
                if self.end == para.depot:
                    self.self_charge()
                    self.is_self_charge = True
                else:
                    self.charge(net)
                    self.is_self_charge = False
            else:
                self.update_location()
                self.is_stand = False
        else:
            self.is_active = False
            self.is_stand = True
            self.is_self_charge = False
        
        
