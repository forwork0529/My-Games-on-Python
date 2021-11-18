# librarys:

from random import *
import copy
import time

# variables:

number_of_ships = [3, 2, 2, 1, 1, 1, 1]
name = None  # Глобальная переменная для вывода имени игрока



class Dot:  #  Класс точка

    def __init__(self, i, j, state=0):
        self.i = i
        self.j = j
        self.state = state

    def state_pls(self):
        return self.state

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def get_coord(self):
        return self.i, self.j


class BoatConstruct:  # Корабельный конструктор

    def __init__(self, i, j, l, r, canv):  # i string, j column , l - lenght, r - round, canv - area
        self.i = i
        self.j = j
        self.l = l
        self.r = r
        self.canv = canv
        self.points = []

    def try_to_stay(self,i, j, l, r, canv):  # canv = game_map
        flag = True
        for l in range(l):
            i = i + (r and l)# if l == True I
            j = j + (not r and l)
            m = len(canv)-1
            if i > m or j > m or not radar1(i, j, canv):
                flag = False
        return flag

    def create_my_boat(self, i, j, l, r : bool, canv):
        self.i = i
        self.j = j
        self.l = l
        self.r = r
        self.canv = canv

        for l in range(self.l):
            i = self.i + (r and l)
            j = self.j + (not r and l)
            self.points.append(self.canv[i][j])
            self.canv[i][j].state  = 8

    def ret_boat_lives(self):
        lives = 0
        for l in self.points:
            if l.state == 8:
                lives += 1
        return lives

    def ret_boat_points(self):
        return self.points


class Board: #  Доска
    def __init__(self, k, fleet):
        self.k = k
        self.fleet = fleet  # палубность и количество кораблей
        self.real_fleet = []  # реальные обьекты состоящие из точек
        self.canv = [[i + j if i * j == 0 else self.k for i in range(7)] for j in range (7)]
        for i in range(1,7):
            for j in range(1,7):
                self.canv[i][j] = Dot(i, j, 0)


        while len(self.real_fleet) < len(number_of_ships): # цикл 1, До тех пор пока все корабли не встали ( при некотрых начальных позициях трёх первых кораблей - 7 корабль поставитььневозможно)
            self.clean_area()
            self.real_fleet = []  # аппендим туда корабли
            for l in (fleet):  # цикл 2, для каждого корабля в отдельности
                trys = 0  # ограничение количества попыток поставить корабль
                continue1 = True  # для завершения попыток поставить корабль если он уже встал
                while continue1 and trys < 72:  # цикл 3, попыток поставить корабль не больше 72
                    k = next(rand_gen1)
                    break2 = False
                    i = k[0]
                    j = k[1]
                    r = (bool(random1() // 3))
                    # print(i, j, r)
                    for _ in range(2):  # цикл 4, если не встал горизонтально - ставь вертикально и наоборот
                        r = r if _ == 0 else not r
                        my_boat = BoatConstruct(i, j, l, r, self.canv)

                        if my_boat.try_to_stay(i, j, l, r, self.canv):
                            my_boat.create_my_boat(i, j, l, r, self.canv)
                            self.real_fleet.append(my_boat)
                            continue1 = False
                            break  #  выход из цикла 4, прерываем for если удалось поставить корабль
                    trys += 1
                     # выход из цикла 3

    def clean_area(self):  # при случайной расстановке без возможности поставить 7 корабль
        k = len(self.canv)
        for i in range(1, k):
            for j in range(1, k):
                self.canv[i][j].state = 0

    def print_area(self , hid = False ):
        map1= copy.deepcopy(self.canv)
        self.hid = hid
        for i in range(len(map1)):
            for j in range(len(map1)):
                if type (map1[i][j]) == int:
                    map1[i][j] = str(map1[i][j])
                else:
                    map1[i][j] = map1[i][j].state
                if map1[i][j] == 8 and hid:
                    map1[i][j] = 0
                # преобразования вида поля , не очень красиво зато понятно
                if type(map1[i][j]) != str:
                    map1[i][j] = Draw.pls(map1[i][j])
        for i in map1:
            print(i)

    def check_herself(self, t : tuple):
        event_dot = Dot(t[0],t[1])
        flotilia = len(self.fleet)
        for b in self.real_fleet:
            if b.ret_boat_lives() == 0:
                flotilia -= 1
                if event_dot in b.ret_boat_points():  # для in переопределён метод __eq__ у класса Dot
                    contur(b.ret_boat_points(),self.canv)
                    jump()
                    print('Корабль убит, вечная память...')
                    time.sleep(3)
                    jump()

        return not(bool(flotilia))

    def shot(self, t : tuple):  # Производит выстрел по полю, возвращает (bool(нужно ли перестреливать), bool (успешен ли выстрел))
        i = t[0]
        j = t[1]
        try:

            a = self.canv[i][j].state
        except:
            jump()
            print(f'Снаряд угодил к соседям, {name}, стреляй ещё раз!')
            time.sleep(2)
            return True, False
        if self.canv[i][j].state == 8:
            self.canv[i][j].state = 9
            jump()
            print(f'Браво {name}! Цель поражена, стреляй ещё раз!')
            time.sleep(2)
            return True, True
        if self.canv[i][j].state == 9 or self.canv[i][j].state == 1:
            jump()
            print(f'Выстрел невозможен,{name}, стреляй ещё раз!')
            time.sleep(2)
            return True, False
        self.canv[i][j].state = 1
        jump()
        print('Пусто...')
        time.sleep(2)
        return False, False

    def vis_flotilia(self):
        my_boats = []
        deck = []
        for b in self.real_fleet:
            for d in b.ret_boat_points():
                deck.append(d.state_pls())
            my_boats.append(deck)
            deck = []
        for i in range(len(my_boats)):
            for j in range(len(my_boats[i])):
                my_boats[i][j] = Draw.pls(my_boats[i][j])
        return my_boats

### Классы и функции помощники ###

class Draw:  # Здесь выбираются символы которыми будут отображатся объекты игровой доски

    a = '_'
    b = '0'
    c = 'B'
    d = 'X'
    @classmethod
    def pls(cls,x):
        if x == 0:
            return cls.a
        if x == 1:
            return cls.b
        if x == 8:
            return cls.c
        if x == 9:
            return cls.d

    @classmethod
    def greetings(cls):
        jump()
        print('Добро пожаловать в игру "Морской бой"')
        time.sleep(3)
        jump()
        print('Правила просты, побеждает тот кто быстрее уничтожит корабли противника.')
        time.sleep(3)
        jump()
        print('Немного о клетках на игровом поле:\n\n')
        print(f'                            Целый корабль  = {cls.c}\n'
              f'                            Корабль подбит = {cls.d}\n'
              f'                            Клетка скрыта  = {cls.a}\n'
              f'                            В клетке пусто = {cls.b}')
        print()
        time.sleep(8)
        jump()
        print('Целимся , задавая сначала строку, затем столбец (цифры от 1 до 6)')
        print('Координаты пишем через "пробел", удачи)')
        time.sleep(6)
        jump()


def contur(boat_points, map):  # функция для обводки уничтоженного корабля
    for dot in boat_points:
        i, j = dot.get_coord()
        for o in range(-1, 2):
            for p in range(-1, 2):
                try:
                    if map[i + o][j + p].state == 0:
                        map[i + o][j + p].state = 1
                except:
                    continue

def radar1(i, j, map : list):  # checking the surroundings for the presence of a ship (return Bool)

    for o in range(-1,2):
        for p in range(-1,2):
            try:
                if map[i+o][j+p].state == 8:
                    return False
            except:
                continue
    return True


def random1():  # простой рандом на 1 число
    return randint(1, 6)

def rand_gen():  # рандом с возвратом 2 х чисел с неповторяющимися значениями до полного прохождения по всем возможным значениям
    l = []
    import random
    while True:
        if len(l) < 1:
            for k in range(1,7):
                l += list(range(k*10 +1 ,k * 10 + 7))

            random.shuffle(l)
        a = l.pop()
        yield a // 10,a % 10

rand_gen1 = rand_gen()

def jump():
    print(60*'\n')



### Игроки и игра ###


class Player:  # creates areas and place ships on it
    def __init__(self,maps:list):
        self.maps = maps
        self.main_area = None
        self.enemy_area = None

class RealPlayer(Player):
    def __init__(self, maps):
        super().__init__(maps)
        self.main_area = maps[0]
        self.enemy_area = maps[1]

    def ask(self):
        i = j = None
        while True:
            try:

                a = input('Куда стреляем? >>>')
                i = int(a[0])
                j = int(a[2])
                break
            except:
                print('Координыты введены с ошибкой')
                continue
        return i , j

    def ret_name(self):
        return "Человек"


class AI(Player):
    def __init__(self, maps):
        super().__init__(maps)
        self.main_area = maps[1]
        self.enemy_area = maps[0]

    def ask(self):
        a = next(rand_gen1)
        i = a[0]
        j = a[1]
        return i , j

    def ret_name(self):
        return "Компьютер"

class Sea_Battle:  # Класс самой игры
    def __init__(self, fleet):
        self.fleet = fleet
        self.maps = [Board(0, self.fleet),Board(0, self.fleet)]
        global name

        player1 = RealPlayer(self.maps) #   AI(self.maps)
        player2 = AI(self.maps)
        big_flag = True
        Draw.greetings()
        while big_flag:
            gamer = eval('player'+str(next(gen8)))

            name = gamer.ret_name()
            jump()
            print(f'{name}, твой ход')
            time.sleep(2)
            print()
            print('Вот твои корабли:')
            print(gamer.main_area.vis_flotilia())
            print()
            print('Вот твоё поле:')
            gamer.main_area.print_area()
            print()
            result_of_shot = (True, False)  # [0] - Нужно ли стрелять , [1] - Успешен ли сделанный выстрел
            while result_of_shot[0]:  # Цикл запускается и для проверки правильности ввода координаты выстрела и возможности произвести выстрел по заданным координатам
                print('Вот поле твоего оппонента:')
                gamer.enemy_area.print_area(True)
                print()

                print()
                coord = gamer.ask()
                result_of_shot = gamer.enemy_area.shot(coord)  # Возвращает [0] True, если нужно стрелять снова, [1] - True , если выстрел успешен
                if result_of_shot[1]:  # Если выстрел успешен проверяем состояние флота

                    if gamer.enemy_area.check_herself(coord):  # если корабль убит - пишем, убиты все - заканчиваем игру
                        big_flag = False
                        break
                jump()
        print(f'Поздравляем - {name} победил')
        print("Игра окончена! Спасибо за игру!")

def gen_player():  # функция (генератор) выбора игрока
    gen = ['1', '2']
    while True:
        gen = gen[::-1]
        yield gen[1]

gen8 = gen_player()



game1 = Sea_Battle(number_of_ships)






















        





