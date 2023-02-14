from random import randint


# ВНИМАНИЮ Менторов
# Во-первых, я вынужден отдать должное красоте этого кода (он крайне элегантен),
# я пока не в состоянии создать такой код, однако в состоянии его прочесть, понять и оценить
# Лично для меня важно, что разбирая код по полочкам, я гораздо глубже стал понимать принципы ООП, чего в курсе явно не хватало
# Большое Вам спасибо за великолепный пример!!!!

# ниже мои скромные доработки исходного кода:

# 1. Добавлена итоговая отрисовка игрового поля после победы игрока или компьютера (прежний код не отрисовывал финальный выстрел)
#    Добавлено цветное оформление финального состояния доски.
# 2. Добавлена опция выбора размера игрового поля (от 4 до 10). Создан дополнительный класс StartMenu/
# 3. При изменении размера игрового поля, шапка с заголовками столбцов автоматически масштабируется
#    до нужного размера; отчеркивания "----" между фазами игры также масштабируются до размеров игрового поля.
#    (При выборе значения игрового поля 10х10 таблица не "расползается" из-за дополнительного символа в 10-ой строке/столбце)
# 4. Исправлен недочет исходного кода, позволяющий стрелять компьютеру только в пределах сетки 6х6
# 5. Количество кораблей на игровом поле меняется в зависимости от размера игрового поля (реализован classmethod: ship_combination)
# 6. Добавлены описания классов и их методов
# 7. Проверка выигрыша скорректирована с учетом количества кораблей на игровом поле
# 8. Закомментированы рудименты, которые не влияют на исход игры:
#       def shooten(self, shot) в классе Ship,
# 9. Исправлен баг, приводящий к генерации носа корабля за пределами игрового поля в методе random_place класса Game:
#    Корректная строка: ship = Ship(Dot(randint(0, self.size-1), randint(0, self.size-1)), l, randint(0,1))

class Dot:
    """
    Класс Dot() - базовый класс, объекты которого определяют положение и назначение точки на игровой доске

    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    #  Внимание стоит уделить магическому методу __eq__, который на первый взгляд не вызывается в явном виде, однако
    #  в ходе пошагового изучения программы обнаружено, что при проверке типа if d in self.busy,
    #  (где d объект класса Dot, a busy - список, элементами которого являются объекты того же класса) осуществялется неявный вызов
    #  def __eq__(self, other)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


#
class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Ship:
    """
    Класс Ship (корабль) принимает в себя три аргумента:
    bow - координаты начала лодки,l - длина корабля, o - булевое значения ориентации корабля (горизонатальное или вертикальное)
    Кроме того, вводится переменная lives, которая определяет количество жизней корабля, равное его длине.

    Класс имеет свойство dots, состоящее из списка ship_dots = [], в который будет записаны координаты создаваемого корабля:
    внутри метода реализуется цикл for, которой проходит по всей длине корабля l
    """

    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            #  в переменные cur_x и cur_y записываются стартовые координаты носа корабля
            cur_x = self.bow.x
            cur_y = self.bow.y
            # Если ориентация корабля =0, то инкрементируется номер строки
            if self.o == 0:
                cur_x += i
            # Если ориентация корабля =1, то инкрементируется номер столбца
            elif self.o == 1:
                cur_y += i
            # Значение координат палуб корабля последовательно записывается в лист ship_dots
            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots
    # здесь был метод-рудимент
    # def shooten(self, shot):
    #     return shot in self.dots


class Board:
    """
    Board - реализует основную игровую логику.
    Принимает параметры:
        hid (от Hidden), т.е. скрывает или отображает корабли на игровой доске;
        size - размерность игровой доски
    В конструкторе класса также определяются следующие параметры:
        self.count - счетчик убитых кораблей
        self.field - список, содержащий стартовое наполнение игрового поля
        self.busy - список, в который записываются координаты занятые кораблем, точек вокруг корабля, координаты выстрелов
        self.ships - список, содержащий координаты кораблей

    Класс содержит следующие методы:
    add_ship(self, ship) - принимает в себя объекты классы Ship(), при удовлетворении ship условиям
                            размещения заполняет списки field, busy, ships и вызывает метод contour(self, ship, verb = False)
    contour(self, ship, verb = False) - принимает объект класса Ship() и параметр видимости и фактически определяет возможные положение точек
                                        (контур) вокруг корабля
    _str__(self) - формирует строку вывода доски игрока и компьютера при вызове, с моими собственными оптимизациями в части формата

    out(self, d) - принимает объект класса Dot. Если координаты выходят за рамки игрового поля, возвращаем True
    shot(self, d) - проверка выстрела на предмет выхода за рамки игрового поля (вызывает метод out())
        #


    """

    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        # список near определяет все возможные положения окрестности точки корабля
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        # цикле проверяет положение окрестности исходной точки переменная cur
        # Если cur в пределах поля и не пресекается со списком занятых позиций в списке busy,
        # то если параметр видимости verb = True, вокруг исходной точки корабля отрисовываются в списке field графический элемент "."
        # также заполняется лист busy позициями этих точек
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    # формирует строку вывода доски игрока и компьютера при вызове, с моими собственными оптимизациями в части формата
    def __str__(self):
        res = "  |"
        for s in range(self.size):
            # Особое форматирование для доски 10*10. Строка отрисовывается без сдвига на доп цифру в числе 10
            if s == 9:
                res += f" {s + 1}|"
            else:
                res += f" {s + 1} |"
        # реализован форматированный вывод наименований строк без сдвига на доп цифру в числе 10
        for i, row in enumerate(self.field):
            res += "{: ^3}".format(f"\n{i + 1}") + "| " + " | ".join(row) + " |"

        # если параметр hid равен True, то скрываем положение кораблей (применяется при вызове доски компьютера)
        if self.hid:
            res = res.replace("■", "O")
        return res

    # Если координаты выходят за рамки игрового поля, возвращаем True
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        # проверка выстрела на предмет выхода за рамки игрового поля
        if self.out(d):
            raise BoardOutException()
        # проверка выстрела на предмет попадания в клетку, выстрел в которую недопустим
        if d in self.busy:
            raise BoardUsedException()
        # после выстрела, удовлетворяющего условиям, осуществляется запись координат точки в лист busy
        self.busy.append(d)
        #  далее в цикле осуществляется проверка попадания в корабль,
        #  если выполнено, то рисуем знак попадания в листе field, и уменьшаем на 1 количество жизней.
        #  Если количество жизней корабля равно нулю, увеличиваем на единицу параметр count (корабль полностью убит).
        #  При этом, если корабль уничтожается, то вызывается метод contour(ship, verb = True) с параметром verb = True,
        #  что позволяет отрисовать точки вокруг корабля, куда не следует стрелять и выводится сообщение об уничтожении корабля.
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True
        #  если промахнулись, то рисуем "."
        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    # Метод вызывается в случае успешной отрисовки корабля на доске и стирает значение листа busy
    def begin(self):
        self.busy = []


class Player:
    """
    Класс игрока, принимающий в качестве параметров экземпляры классов собственной игровой доски и доски противника
    """

    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    # Метод move, реализующий вызов метода shot объекта класса board,
    # где в качестве параметра передается результат выполнения метода ask()
    def move(self):
        while True:
            try:
                target = self.ask()
                # repeat принимает значение True или False в зависимости от результатов выстрела,
                # если True (т.е. стреляющий попал в корабль) предоставляется дополнительный ход.
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    """
    Класс AI (компьютер) дочерний класс родительского класса PLayer
    Переопределяет функцию ask.
    Для компьютера в рамках метода ask создается объект класса Dot с рандомным определением координат X, Y,
    которые затем передаются в метод shoot (выстрел) класса Board
    """

    def ask(self):
        d = Dot(randint(0, g.size - 1), randint(0, g.size - 1))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    """
    Класс User(Player) наследует методы класса Player() и
    переопределяет метод ask() следующим образом:
    в цикле while у игрока запрашиваются координаты выстрела, метод возвращает объект класса Dot() c координатами
    """

    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    """
     В данном классе по умолчанию инициализируются переменная размерности игрового поля,
     а также два объекта pl и co, которые по сути являются экземплярами класса Board игрока и компьютера.
     Далее объекту класса "co" присваивается значение hid = True (от Hidden), т.е. доска компьютера делается скрытой
     Также инициализируются два объекта класса Player (self.ai = AI(co, pl) и self.us = User(pl, co)),
     в которые в качестве аргументов помещаются состояния досок Компьютера и Игрока.
    """

    def __init__(self, size=6):
        self.size = size
        self.lens = self.ship_combination(size)
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    #  метод ship_combination определяет набор кораблей,
    #  исходя из размеров игрового поля (size), выбранного пользователем
    @classmethod
    def ship_combination(cls, size):
        # lens = []
        if 4 <= size <= 10:
            ship_var = {4: [2, 1, 1],
                        5: [2, 1, 1, 1, 1],
                        6: [3, 2, 2, 1, 1, 1, 1],
                        7: [3, 2, 2, 2, 1, 1, 1, 1],
                        8: [3, 3, 2, 2, 1, 1, 1, 1],
                        9: [3, 3, 2, 2, 2, 1, 1, 1, 1],
                        10: [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]}
            lens = ship_var.get(size)
        return lens

    # random_board в бесконечном цикле вызывает метод random_place,
    # в рамках которого рандомно создаются корабли ship на досках Board игрока и компьютера,
    # это необходимо для того, чтобы если в течение 2 тыс. итераций не получилось создать корабль,
    # соответсвующий условиям размещения корабля на игровом поле, запустить цикл заново.
    #
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    #
    # Функция random_place определяет локальный список lens = [3, 2, 2, 1, 1, 1, 1],
    # элементами которого являются длины кораблей (3 - три клетки занимает, 1 - одну клетку),
    # количество элементов списка, соответственно, определяет количество кораблей.
    # Создается объект класса board = Board(size = self.size), с параметров size равный 6
    # В цикле for пробегающийся по элементам списка lens  и вложенном цикле while (осуществляющим 2000 попыток создания корабля)
    # создается объект класса Ship, принимающий в качестве параметров, координаты начала лодки Dot(randint(0, self.size), randint(0, self.size))
    # длину лодки l и ориентацию лодки на игровом поле (горизонтальная или вертикальная),
    # далее в конструкции try-except осуществляется проверка возможности размещения созданного корабля на игровой доске
    # при этом сам BoardWrongShipException по сути пустой.
    # После успешного создания запускает метод board.begin() и результатом работы random_place возвращается объект board класса Board(),
    #

    def random_place(self):
        lens = self.lens
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                # генерация объекта ship класса Ship()
                ship = Ship(Dot(randint(0, self.size - 1), randint(0, self.size - 1)), l, randint(0, 1))
                try:
                    # Если параметры корабля, выходят за рамки игрового поля
                    # или не соблюдается принцип расположения кораблей друг относительно друга, то отрабатывает exception
                    # и цикл создания корабля начинается заново
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        # после успешного создания корабля инициализируется метод begin() класса Board, в рамках которого очищается состояние листа busy = []
        board.begin()
        return board

    # В методе loop последовательно отрисовываются доски игрока и компьютера,
    # при этом очередность хода определяется состояние переменной num:
    # для четных num - ходит игрок, для нечетных компьютер, тем самым обеспечивается переход хода от игрока к компьютеру и наоборот
    # если игрок или компьютер попал в корабль, то переменная num декрементируется,
    # тем самым позволяя игроку или компьютеру сделать повторный ход.
    # Сам ход реализуется посредством вызова метода repeat = self.us.move(),
    # возращающего True или False в зависимости от результата выстрела.
    # Количество подбитых кораблей фиксируется в переменной board.count,
    # при достижении значения равного количеству подбитых кораблей фиксируется победа игрока или компьютера
    def loop(self):
        num = 0
        while True:
            print("---" + "-" * 4 * self.size)
            print("Доска пользователя:")
            print(self.us.board)
            print("---" + "-" * 4 * self.size)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("---" + "-" * 4 * self.size)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("---" + "-" * 4 * self.size)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            # Добавлен форматированный вывод в консоль сообщения о победе и финального состояния доски
            if self.ai.board.count == len(self.lens):
                print("---" + "-" * 4 * self.size)
                print("\033[7m{}\033[0m".format("Пользователь выиграл!"))
                print("\033[36m{}\033[0m".format(self.ai.board))
                break

            if self.us.board.count == len(self.lens):
                print("---" + "-" * 4 * self.size)
                print("\033[7m{}\033[0m".format("Компьютер выиграл!"))
                print("\033[36m{}\033[0m".format(self.us.board))
                break
            num += 1

    def start(self):
        # self.greet()
        self.loop()


class StartMenu:
    """
    Класс StartMenu определяет стартовые параметры взаимодействия с пользователем
    в настоящий момент реализован двумя методами:
    greet() - выводит приветственное сообщение и правила игры
    board_choise() - метод определения размера игрового поля через взаимодействие с игроком,
                     После исполнения метод возвращает параметр size, который в дальнейше будет передан в объект класса Game()
    """

    def greet(self):
        print("-------------------")
        print("  Приветствуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
        print("-------------------")

    @classmethod
    def board_choise(cls):
        print("Размер игрового поля по умолчанию - 6х6.")
        print("Для подтверждения нажмите Enter,")
        while True:
            size = input("для изменения введите число от 4 до 10: ")
            if size == "":
                size = 6
                return size
            if not (size.isdigit()):
                print("Введите число! ")
                continue
            size = int(size)
            if not (4 <= size <= 10):
                print(" Введите число в диапазоне от 4 до 10 ")
                continue
            return size
# ***************************************************************************************
s = StartMenu()
s.greet()

g = Game(s.board_choise())
g.start()