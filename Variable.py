import Star
import JDN
from decimal import Decimal

__author__ = "Moskvin Vasiliy (vasiliy.moscvin@yandex.ru)"


class Variable(Star.Star):
    def __init__(self, name, ra, dec, period, epoch_center, t_duration):
        super().__init__(name, ra, dec)
        epoch_center = Decimal(epoch_center)
        self.period = Decimal(period)
        self.t_duration = Decimal(t_duration)
        self.epoch = (epoch_center - self.t_duration / 2,
                      epoch_center,
                      epoch_center + self.t_duration / 2)

    def __str__(self):
        return 'name = {} ra = {:.7f} dec = {:.7f} period = {:.7f} ' \
               'epoch_center = {:.7f} transit duration = {:.7f}'.format(self.name,
                                                                        self.ra,
                                                                        self.dec,
                                                                        self.period,
                                                                        self.epoch[1],
                                                                        self.t_duration)

    def get_ephemerid(self, epoch):
        """
        Возвращает следующую эфемериду, по указанной эпохе
        :param epoch: эпоха
        :return: следующая эфемерида
        """
        return epoch + self.period

    def get_next_ephemerid(self, *key):
        """
        Возвращает значения следующей эфемериды по ключу (s, c, e). Если ключ не указан, то возвращается
        кортеж значений эфемерид: s - start, c - center, e - end
        :param key: эфемериду чего считать: start, center, end
        :return: эфемериды
        """
        if not key:
            return tuple(map(lambda x: x + self.period, self.epoch))
        elif key[0] == "s":
            return self.get_ephemerid(self.epoch[0])
        elif key[0] == "c":
            return self.get_ephemerid(self.epoch[1])
        elif key[0] == "e":
            return self.get_ephemerid(self.epoch[2])
        else:
            raise Star.KeyInputError

    def get_list_ephemerids(self, n, *key):
        """
        Возвращает список n следующих эфемерид, отсчитывая от: начала (s), центра (c) или конца (e) изменения блеска
        :param n: количество эфемерид
        :param key: ключ, указывающий начало отсчёта s - start, c - center, e - end, отсутствие ключа - возвращает
                    эфемериды для всех трёх точек
        :return: список эфемерид
        """
        if not key:
            eph = self.epoch
        elif key[0] == "s":
            eph = self.epoch[0]
        elif key[0] == "c":
            eph = self.epoch[1]
        elif key[0] == "e":
            eph = self.epoch[2]
        else:
            raise Star.KeyInputError
        if type(eph) == tuple:
            lst = [[], [], []]
            for i in range(n):
                for index, src in enumerate(eph):
                    lst[index].append(self.get_ephemerid(src))
                eph = [x + self.period for x in eph]
        else:
            lst = []
            for i in range(n):
                lst.append(self.get_ephemerid(eph))
                eph += self.period
        return lst


COROT_2b = Variable("COROT_2b", "19 27 6.494", "1 23 1.17", 1.7429964, 2454706.4016, 0.095)


# print(COROT_2b)
# try:
#    lst = COROT_2b.get_list_ephemerids(10)
# except Star.KeyInputError:
#    print("Ошибка ключа. Нет такого ключа!")
# else:
#    if type(lst[0]) == list:
#        for i in zip(lst[0], lst[1], lst[2]):
#            print("{} {} {}".format(*i))
#    else:
#        for i, src in enumerate(lst):
#            print("{}: {}".format(i, src))


def sort_phemerides(*stars, n, key):
    """
    Возвращает отсортированный список звёзд по их эфемеридам.
    Возможны два случая: сортируется по какому-либо только по одному ключу(s, c, e)
    или сортируются по всем трём ключам (ключ a)
    :param stars: кортеж звёзд
    :param n: количество эфемерид от указанных эпох для каждой звезды
    :param key: ключи (s - start, c - center, e - end, a - all)
    :return: отсортированный список звёзд по их эфемеридам
    """
    lst_dict = []
    lst = [[], [], []]
    if key == "a":
        for i in stars:
            lst_dict.append({"name": i.name,
                             "s": i.get_list_ephemerids(n, "s"),
                             "c": i.get_list_ephemerids(n, "c"),
                             "e": i.get_list_ephemerids(n, "e")})

        for i in lst_dict:
            lst[2].extend(i["s"])
            lst[2].extend(i["c"])
            lst[2].extend(i["e"])
        lst[2].sort()
        flag = False

        for i in lst[2]:
            for j in lst_dict:
                for keys in j.keys():
                    if keys != "name":
                        if i in j[keys]:
                            lst[0].append(j["name"])
                            lst[1].append(keys)
                            flag = True
                            break
                    if flag:
                        flag = False
                        break
        return lst

    elif key == "s" or key == "c" or key == "e":
        for i in stars:
            lst_dict.append({"name": i.name,
                             key: i.get_list_ephemerids(n, key)})
        for i in lst_dict:
            lst[2].extend(i[key])
        lst[2].sort()

        for i in lst[2]:
            for j in lst_dict:
                if i in j[key]:
                    lst[0].append(j["name"])
                    lst[1].append(key)
                    break
        return lst
    else:
        raise Star.KeyInputError


st = Variable("one", "19 27 6.494", "1 23 1.17", 1.2198669, 2457725.1784722, 0.095)
st1 = Variable("two", "19 27 6.494", "1 23 1.17", 1.4200246, 2457725.1618056, 0.095)
st2 = Variable("tre", "19 27 6.494", "1 23 1.17", 3.2130598, 2457728.6958333, 0.095)

lst = sort_phemerides(st, st1, st2, n=20, key="a")

for i in zip(*lst):
    print("{}\t{}\t{}".format(i[0], i[1], JDN.get_formated_GD(str(i[2]))))
