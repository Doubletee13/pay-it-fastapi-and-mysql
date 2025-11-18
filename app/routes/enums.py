# All Enum here
from enum import Enum


class Category(str, Enum):
    FARMER = "farmer"
    BUYER = "buyer"


class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"
    
