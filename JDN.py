from math import modf


def get_JDN(year, month, day):
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    JDN = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    return JDN


def get_JD(year, month, day, h, m, s):
    return get_JDN(year, month, day) + (h - 12) / 24 + m / 1440 + s / 86400


def get_GD(JD):
    Z = int(JD.split(".")[0])
    F = round(float(JD) - Z, 6)
    if Z < 2299161:
        A = Z
    else:
        alfa = (Z - 1867216.25) // 36524.25
        A = Z + 1 + alfa - alfa // 4
    B = A + 1524
    C = (B - 122.1) // 365.25
    D = int(365.25 * C)
    E = (B - D) // 30.6001
    ost, day = modf(B - D - int(30.6001 * E) + F)
    day = int(day)
    hours = int(ost * 24)
    minuts = int((ost - hours / 24) * 1440)
    seconds = int((ost - hours / 24 - minuts / 1440) * 86400)
    if E < 13.5:
        month = int(E - 1)
    else:
        month = int(E - 13)
    if month > 2.5:
        year = int(C - 4716)
    else:
        year = int(C - 4715)
    if hours > 11:
        day += 1
        hours -= 12
    else:
        hours += 12
    return day, month, year, hours, minuts, seconds

def get_formated_GD(JD):
    tpl = get_GD(JD)
    return "{}/{}/{}\t{}:{}:{}".format(*tpl)


if __name__ == "__main__":
    lst = get_GD('2454706.3542')
    print("{}/{}/{}\t{}:{}".format(*lst))
    #    list_date = [int(i) for i in input("d m y").split()]
    #    list_day = [float(i) for  i in input("h m s").split()]
    #    print(get_JDN(list_date))
    #    print(round(get_JD(get_JDN(list_date), list_day[0], list_day[1], list_day[2]), 7))
    print(round(get_JD(2016, 12, 2, 16, 17, 00), 7))
    print(round(get_JD(2016, 12, 2, 15, 53, 00), 7))
    print(round(get_JD(2016, 12, 6, 4, 42, 00), 7))

# 2454706.3542 27/8/2008	20:30
# 2454706.4016 27/8/2008	21:38
# 2454706,4491 27/8/2008	22:46

