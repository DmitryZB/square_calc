import matplotlib.pyplot as plt

# Убираем надоедливые предупреждения от matplotlib
import warnings

warnings.filterwarnings("ignore")


# Функция решения квадратного уравнения по его коэффициентам
def Solver(coefs):
    # Проверка на наличие коэффициентов
    if coefs is None:
        return None

    a = coefs['a']
    b = coefs['b']
    c = coefs['c']
    if a == b == 0:
        return None
    elif a == c == 0 or b == c == 0:
        return 0

    # Частный случай - линейное уравнение
    elif a == 0:
        return -c / b

    # Частный случай - неполное квадратное уравнение
    elif b == 0:
        if c <= 0:

            # Создение кортежа корней уравнения
            answers = (-(-c) ** 0.5 / a, (-c) ** 0.5 / a)
            return answers
        else:
            return None
    elif c == 0:

        # Создение кортежа корней уравнения
        answers = (0, -b / a)
        return answers

    # Решение полного квадратного уравнения через дискриминант
    D = b ** 2 - 4 * a * c
    if D < 0:
        return None
    if D == 0:
        return -b / (2 * a)

    # Создение кортежа корней уравнения
    answers = ((-b - D ** 0.5) / (2 * a), (-b + D ** 0.5) / (2 * a))
    return answers


# Функция для построения графика
def Graph(coefs):
    # Проверка на наличие коэффициентов
    if coefs is None:
        return None

    a = coefs['a']
    b = coefs['b']
    c = coefs['c']

    # Списки точек графика
    x_list = []
    y_list = []

    if a != 0:
        x_middle = -b / (2 * a)
    elif b != 0:
        x_middle = -c / b
    else:
        x_middle = 0

    # Заполнение списков точек графкика
    for i in range(int(x_middle - 50), int(x_middle + 50)):
        x_list.append(i)
        y_list.append(a * i ** 2 + b * i + c)

    # Инициализация графика и его отображение
    fig, ax = plt.subplots()
    ax.plot(x_list, y_list, 'r', linewidth=2.0)
    ax.set_xlabel('x')
    ax.set_ylabel('y(x)')
    ax.set_title(f'y = {a}x^2 + ({b}x) + ({c})')
    ax.grid()
    plt.show()


# Функция проверки правильности введенного уравнения
# и отделения коэффициентов
def Checker(data):
    # Словарь коэффициентов
    coefficients = {'a': 0, 'b': 0, 'c': 0}
    length = len(data)
    buf = 0  # Переменная считывания чисел
    is_minus = 0  # Индикатор знака минус
    is_plus = 0  # Индикатор знака плюс
    skip_counter = 0  # Счетчик пропускаемых символов
    is_left_side = True  # Индикатор левой части уравнения
    sign_check = True

    # Цикл посимвольного перебора строки (уравнения)
    for i in range(length):

        if skip_counter:
            skip_counter -= 1
            continue

        elif not is_minus and data[i] == '-':
            is_minus = 1
            sign_check = True
            continue

        elif data[i] == '+' and not is_plus:
            is_plus = 1
            sign_check = True
            continue

        elif data[i] == '=' and is_left_side:
            is_left_side = False
            sign_check = True
            continue

        # Запись числа, если символ - цифра
        elif '9' >= data[i] >= '0':
            if not sign_check:
                print("Отсутствует арифметический знак!")
                return
            buf *= 10
            if buf < 0:
                buf -= int(data[i])
            else:
                buf += int(data[i])
            if is_minus == 1:
                buf *= -1
                is_minus = 2

            if i == len(data) - 1:
                if is_left_side:
                    coefficients['c'] += buf
                else:
                    coefficients['c'] -= buf
                buf = 0
            elif data[i + 1] == "=" or data[i + 1] == "-" or data[i + 1] == "+":
                if is_left_side:
                    coefficients['c'] += buf
                else:
                    coefficients['c'] -= buf
                buf = 0
                is_minus = 0
                is_plus = 0
            continue

        # Сохраняем записанное число в соответствующую
        # переменную коэффициента
        elif data[i] == 'x':
            if i == len(data) - 1:
                if is_left_side:
                    if buf == 0 and (i == 0 or data[i - 1] != '0'):
                        if not is_minus:
                            coefficients['b'] += 1
                        if is_minus:
                            coefficients['b'] -= 1
                    else:
                        coefficients['b'] += buf
                else:
                    if buf == 0 and (i == 0 or data[i - 1] != '0'):
                        if not is_minus:
                            coefficients['b'] -= 1
                        if is_minus:
                            coefficients['b'] += 1
                    else:
                        coefficients['b'] -= buf
                buf = 0
            elif i == len(data) - 2:
                print("Неверный синтаксис: неверная правая часть!")
                return

            # Случай, когда коэффициент стоит перед
            # квадратом переменной (запись коэффициента а)
            elif data[i + 1: i + 3] == "^2":
                if is_left_side:
                    if buf == 0 and (i == 0 or data[i - 1] != '0'):
                        if not is_minus:
                            coefficients['a'] += 1
                        else:
                            coefficients['a'] -= 1
                    else:
                        coefficients['a'] += buf
                else:
                    if buf == 0 and (i == 0 or data[i - 1] != '0'):
                        if not is_minus:
                            coefficients['a'] -= 1
                        else:
                            coefficients['a'] += 1
                    else:
                        coefficients['a'] -= buf
                skip_counter = 2
                buf = 0
                is_minus = 0
                is_plus = 0
                sign_check = False

            # Случай, когда коэффициент стоит перед переменной
            # (запись коэффициента b)
            elif data[i + 1: i + 3] == "^1":
                if is_left_side:
                    if buf == 0 and (i == 0 or data[i - 1] != '0'):
                        if not is_minus:
                            coefficients['b'] += 1
                        else:
                            coefficients['b'] -= 1
                    else:
                        coefficients['b'] += buf
                else:
                    if buf == 0 and (i == 0 or data[i - 1] != '0'):
                        if not is_minus:
                            coefficients['b'] -= 1
                        else:
                            coefficients['b'] += 1
                    else:
                        coefficients['b'] -= buf
                skip_counter = 2
                buf = 0
                is_minus = 0
                is_plus = 0
                sign_check = False

            # Случаи, когда коэффициент свободный (запись коэффициента с)
            elif data[i + 1: i + 3] == "^0":
                if is_left_side:
                    if buf == 0 and (i == 0 or data[i - 1] != '0'):
                        if not is_minus:
                            coefficients['c'] += 1
                        else:
                            coefficients['c'] -= 1
                    else:
                        coefficients['c'] += buf
                else:
                    if buf == 0 and (i == 0 or data[i - 1] != '0'):
                        if not is_minus:
                            coefficients['c'] -= 1
                        else:
                            coefficients['c'] += 1
                    else:
                        coefficients['c'] -= buf
                skip_counter = 2
                buf = 0
                is_minus = 0
                is_plus = 0
                sign_check = False
            elif data[i + 1] == "=" or data[i + 1] == "-" or data[i + 1] == "+":
                if is_left_side:
                    if buf == 0 and (i == 0 or data[i - 1] != '0'):
                        if not is_minus:
                            coefficients['b'] += 1
                        else:
                            coefficients['b'] -= 1
                    else:
                        coefficients['b'] += buf
                else:
                    if buf == 0 and (i == 0 or data[i - 1] != '0'):
                        if not is_minus:
                            coefficients['b'] -= 1
                        else:
                            coefficients['b'] += 1
                buf = 0
                is_minus = 0
                is_plus = 0

        # Символ не является ни переменной, ни числом, ни допустимым знаком
        else:
            print(f"Неверный синтаксис на символе: {data[i]}!")
            return

    # Вывод упрощенного уравнения с вычисленными коэффициентами
    print(f"Упрощенное уравнение: {coefficients['a']}x^2 + "
          f"({coefficients['b']}x) + ({coefficients['c']}) = 0")
    return coefficients


# Точка входа программы
if __name__ == '__main__':
    data = input("Введите квадратное уравнение типа a*x^2 + b*x + c: ")
    print("Введеное уравнение:", data)

    # Проверка правильности расположения знаков "умножить"
    if data.find("*x") != data.find("*"):
        print("Неверный синтаксис!")
    else:

        # Форматирование строки путем удаления пробелов и знаков "умножить"
        data = data.replace(' ', '').replace('*', '')
        coefficients = Checker(data)
        answer = Solver(coefficients)
        print("Корни уравнения: ", answer)
        Graph(coefficients)
