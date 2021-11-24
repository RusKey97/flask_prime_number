def split_places(number):
    """Разбиение числа по разрядам"""
    if number is None:
        return number
    
    str_number = str(number)
    res = []  # массив с ответом
        
    while str_number:
        res.append(str_number[-3:])
        str_number = str_number[:-3]
    return' '.join(reversed(res))

def is_prime(n):
    """является ли число простым (возвращается булево значение)"""
    for i in range(2, int(n ** 0.5) + 1):
        if not n % i:
            return False
    return True and n != 1  # 1 является  ни простым, ни составным

def is_prime_text(n):
    """является ли число простым (возвращается текстовая строка)"""
    if n == 1:
        return 'Ни простое, ни составное'
    return 'Простое' if is_prime(n) else 'Составное'

def prev_prime(n):
    """вычисление предыдущего простого числа"""
    n -= 1
    if n < 2:
        return None
    while True:
        if is_prime(n):
            return n
        n -= 1

def next_prime(n):
    """вычисление следующего простого числа"""
    n += 1
    while True:
        if is_prime(n):
            return n
        n += 1

def range_prime(n):
    return [prev_prime(n), next_prime(n)]

def decompose(n):
    """разложение числа на простые множители"""
    if n == 1:
        return '1 = 1'
        
    parts = []  # массив множителей
    temp = n  # в процессе работы необходимо изменять неперменную, но также сохранить для вывода
    now = 2  #  первое простое число
    
    while temp != 1:
        if temp % now == 0:
            parts.append(str(now))
            temp //= now
        else:
            now = next_prime(now)
    return [str(i) for i in parts]  # ответом явлается массив строк из чисел