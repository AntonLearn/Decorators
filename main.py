import os
import datetime


def logger(old_function):
    def new_function(*args, **kwargs):
        dt_now = datetime.datetime.now()
        result = old_function(*args, **kwargs)
        with open('main.log', 'a') as file:
            file.write(f'Функция: {old_function.__name__} с аргументами: {args} и {kwargs}:\n')
            file.write(f'   Дата и время вызова функции: {dt_now}\n')
            file.write(f'   Возвращаемое значение: {result}\n')
        return result
    return new_function


# Тест задания 1
def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'
    @logger
    def summator(a, b=0):
        return a + b
    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def logger_params(path):
    def _logger_params(old_function):
        def new_function(*args, **kwargs):
            dt_now = datetime.datetime.now()
            result = old_function(*args, **kwargs)
            with open(path, 'a') as file:
                file.write(f'Функция: {old_function.__name__} с аргументами: {args} и {kwargs}:\n')
                file.write(f'   Дата и время вызова функции: {dt_now}\n')
                file.write(f'   Возвращаемое значение: {result}\n')
            return result
        return new_function
    return _logger_params


# Тест задания 2
def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_params(path)
        def hello_world():
            return 'Hello World'

        @logger_params(path)
        def summator(a, b=0):
            return a + b

        @logger_params(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


# Тест задания 3
def test_3():
    path = 'log_params.log'

    if os.path.exists(path):
        os.remove(path)

    @logger_params(path)
    def exp_of_num(**kwarg):
        a, n = kwarg.values()
        val = 1
        for i in range(n):
            val *= a
        return val

    assert 1024 == exp_of_num(a=2, n=10), "Функция возвращает 2^10=1024"
    assert 9 == exp_of_num(a=3, n=2), "Функция возвращает 3^2=9"
    assert 125 == exp_of_num(a=5, n=3), "Функция возвращает 5^3=125"


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
