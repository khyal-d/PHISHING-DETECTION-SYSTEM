from .packages import *

with open("data/allbrands.txt", "r") as f:
    allbrand = [line.strip().lower() for line in f if line.strip()]


 