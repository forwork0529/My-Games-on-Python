# variables:
p = []


def game_start():
    global p
    p = canvas()
    player = None
    typed = ' '
    print("Игра крестики началась!")
    refresh_canvas(p)
    while True:

        player = next(gen1)
        move(player)
        refresh_canvas(p)
        if end_of_the_game(p):
            print(f'Игрок {player} победил!')
            return
        t = 0 # переменная счётчик заполненных регистров
        for f in range(4):
            if '-' not in p[f]:
                t += 1
                if t == 4:
                    print('Победила дружба')
                    return



def canvas(): # функция рисующая пустое поле

    p =([[str((i+j)-1 if (i+j)-1 >= 0 else ' ') if i*j == 0 else '-'\
        for j in range(4)]for i in range (4)])
    return p

"""
for debug:

        [[' ', '0', '1', '2'],\
         ['0', 'X', 'X', 'O'],\
         ['1', 'X', 'X', 'O'],\
         ['2', 'O', 'O', '-']]
"""

def gen_player(): # функция выбора игрока
    gen = ['X','O']
    while True:
        gen = gen[::-1]
        yield gen[1]
gen1 = gen_player()


def refresh_canvas(p): # функция обновления поля после каждого хода
    for k in p:
        print(k)

def move(player):
    while True:
        print(f'Игрок {player} твой ход!')
        typed = input('Напишите координаты через пробел, например: "1 0"')
        x = int(typed[0])+1
        y = int(typed[2])+1

        if (x <= 3) and (y <= 3) and (p[x][y] != 'X' and p[x][y] != 'O'):
            break
    p[x][y] = player

def end_of_the_game(v): # условия завершения игры
    flag = False
    c = 0 # выигрыш по горизонтали
    d = 0 # выигрыш по вертикали
    l = 0 # выигрышь по диагонали
    h = 0 # выигрышь по диагонали
    for j in range(1, 4): # strings
        for i in range(1, 4): # columns

            if v[j][i] != v[j][i - 1] or v[j][i] == '-':
                c = 0
            else:
                c += 1

            if v[i][j] != v[i - 1][j] or v[i][j] == '-':
                d = 0
            else:
                d += 1
            if c == 2 or d == 2:
                flag = True

    for i in range(1, 3): # цикл для расчёта диагоналей

        if v[i + 1][i + 1] != v[i][i] or v[i][i] == '-':
            l = 0
        else:
            l += 1
        if v[4 - i][0 + i] != v[3 - i][1 + i] or v[4 - i][0 + i] == '-':
            h = 0
        else:
            h += 1
        if l == 2 or h == 2:
             flag = True
    return flag

game_start() # Ну погнали)!






