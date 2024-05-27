from enum import Enum

class Routes(Enum):
    INDEX = "route_index"
    PREDICT = "route_predict"
    TRAIN = "route_train"
    ABOUT = "route_about"

class Rules(Enum):
    INDEX = "/"
    PREDICT = "/predict"
    TRAIN = "/train"
    ABOUT = "/about"
