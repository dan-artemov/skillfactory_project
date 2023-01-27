# Функция, отрисовывающая игровое поле
def show():
    print(1, 2, 3)
    i = 1
    for y in field:
        for x in y:
            print(x, end=" ")
        print(i, '')
        i += 1
# Функция ввода координат ячейки и проверки ошибок ввода

def input_data():
    while True: # реализуем бесконечный цикл для проверки введенных Игроком данных
        x = input('введите значение координаты по оси Х (1, 2 или 3): ')
        y = input('введите значение координаты по оси Y (1, 2 или 3): ')
        if not(x.isdigit()) or not(y.isdigit()):
            print("----------Ошибка. Введите числа----------")
            continue
        x, y = int(x), int(y)
        if x < 1 or x > 3 or y < 1 or y > 3:
            print("----------Ошибка. Координаты вне диапазона игрового поля, повторите ввод данных----------")
            continue

        if field[y-1][x-1] != '-':
            print('----------Данная клетка уже занята, повторите ввод данных----------')
            continue
        return x, y




# Функция проверки выигрышных комбинаций
def check_win():
    win_position = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)),
                    ((2, 0), (2, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                    ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
                    ((0, 0), (1, 1), (2, 2)), ((2, 0), (1, 1), (0, 2)))
    for A in win_position:
        check = []
        for B in A:
            check.append(field[B[0]][B[1]])
        if check == ['X', 'X', 'X']:
            print('Победили Крестики')
            return True
        if check == ['0', '0', '0']:
            print('Победили Нолики')
            return True
    return False

# Основной цикл игрового процесса (9 ходов)
field = [['-','-','-'],
        ['-','-','-'],
        ['-','-','-'],]

print('------ИГРА-----')
print('крестики-нолики')
print('')
show()
print('')
for i in range(1, 10):

    if i % 2 == 1:
        print(f'Ход-{i}. Крестики')
        x, y = input_data()
        field[y-1][x-1]='X'
    else:
        print(f'Ход-{i}. Нолики')
        x, y = input_data()
        field[y - 1][x - 1] = '0'
    show()
    print('')
    if i >= 5 and check_win():
        break
    if i == 9 and not check_win():
        print('!!!Ничья!!!')
show()
print('')
# input_data()