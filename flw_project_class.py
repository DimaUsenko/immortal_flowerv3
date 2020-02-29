from pysolar.solar import *
import math
import numpy as np

class Sun(object):
    def __init__(self, latitude, longitude, date):
        self.lat = latitude
        self.long = longitude
        self.date = date
        self.alt = math.radians(get_altitude(self.lat, self.long, self.date))
        self.azt = math.radians(get_azimuth(self.lat, self.long, self.date))
        self.r = 300
        self.x = self.r * math.cos(self.alt) * math.cos(self.alt)
        self.y = self.r * math.cos(self.alt) * math.sin(self.azt)
        self.z = self.r * math.sin(self.alt)

    def vec(self):
        self.x = self.r * math.cos(self.alt) * math.cos(self.azt)
        self.y = self.r * math.cos(self.alt) * math.sin(self.azt)
        self.z = self.r * math.sin(self.alt)
        vec = np.array([self.x, self.y, self.z])
        return vec


class Lamp(object):
    def __init__(self):
        self.work = False

    def on(self):
        self.work = True

    def off(self):
        self.work = False

    def check(self):
        if (self.work):
            return "ON"
        else:
            return "OFF"


class Cloud(object):
    def __init__(self, center_of_cloud_x, center_of_cloud_y, height_cloud, speed_x, speed_y, const_x, const_y):
        self.x_center = center_of_cloud_x
        self.y_center = center_of_cloud_y
        self.z = height_cloud
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.x1 = center_of_cloud_x + const_x
        self.y1 = center_of_cloud_y + const_y
        self.x2 = center_of_cloud_x + const_x
        self.y2 = center_of_cloud_y - const_y
        self.x3 = center_of_cloud_x - const_x
        self.y3 = center_of_cloud_y - const_y
        self.x4 = center_of_cloud_x - const_x
        self.y4 = center_of_cloud_y + const_y

    def vec(self):
        return np.array([[self.x1, self.y1, self.z],
                         [self.x2, self.y2, self.z],
                         [self.x3, self.y3, self.z],
                         [self.x4, self.y4, self.z]])

    def move(self):

        self.x1 = self.x1 + self.speed_x
        self.y1 = self.y1 + self.speed_y
        self.x2 = self.x2 + self.speed_x
        self.y2 = self.y2 + self.speed_y
        self.x3 = self.x3 + self.speed_x
        self.y3 = self.y3 + self.speed_y
        self.x4 = self.x4 + self.speed_x
        self.y4 = self.y4 + self.speed_y

    def getx(self):
        return [self.x1, self.x2, self.x3, self.x4]

    def gety(self):
        return [self.y1, self.y2, self.y3, self.y4]

    def getz(self):
        return [self.z, self.z, self.z, self.z]


class Flower(object):
    def __init__(self, x0, y0, z0):
        self.x = x0
        self.y = y0
        self.z = z0

    def point(self):
        return np.array([self.x, self.y, self.z])
