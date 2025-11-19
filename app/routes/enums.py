# All Enum here
from enum import Enum


class Category(str, Enum):
    FARMER = "farmer"
    BUYER = "buyer"


class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"

class ProductType(str, Enum):
    GRAINS = "grains"
    TUBERS = "tubers"
    VEGETABLES = "vegetables"
    FRUITS = "fruits"
    LIVESTOCK = "livestock"
    CEREALS = "cereals"
    LATEX = "latex"
    OILS = "oils"




    
