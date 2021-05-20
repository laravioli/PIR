import sys

sys.path.append("C:\\Users\\Victor\\Desktop\\PIR\\data")

import math
from utils import *


def date_process(date):

    frac, year = math.modf(date)
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        days = 366
    else:
        days = 365
    days = frac * days
    frac, days = math.modf(days)
    hours = frac * 24
    frac, hours = math.modf(hours)
    minutes = frac * 60
    frac, minutes = math.modf(minutes)
    secondes = frac * 60

    print(
        "years:{}"
        "days:{}, hours:{}, minutes:{}, secondes{}".format(
            year, days, hours, minutes, secondes
        )
    )


data1, meta1 = read("data/NPOES_DATA/NPOES14_SEM_PROT_2500keV_1998.map")
data2, meta2 = read("data/NPOES_DATA/NPOES15_SEM2_PROT_2500keV_1998.map")

for date1, date2 in zip(meta1["x"][362:], meta2["x"][:]):
    date_process(date1)
    date_process(date2)
    print("_______________________________________________")
