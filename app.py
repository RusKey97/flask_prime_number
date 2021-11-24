from flask import Flask, render_template, redirect, url_for, abort, request
from config import Config
from forms.coder_form import CoderForm
from prime_functions import *


app = Flask(__name__)
app.config.from_object(Config)
QUOTE_CH = '\''

operations_id_dict = {0 : 'is_prime',
                      1 : 'prev_prime',
                      2 : 'next_prime',
                      3 : 'range_prime',
                      4 : 'decompose'}

operations_function_dict = {'is_prime' : is_prime_text,
                            'prev_prime' : prev_prime,
                            'next_prime' : next_prime,
                            'range_prime' : range_prime,
                            'decompose' : decompose}

def format_result(number, operation, result, split_places_flag, explanatory_message):
    """Форматирование строки с ответом"""
    
    # если необходимо разбивать разряды чисел
    if split_places_flag:
        number = split_places(number)
        if operation in ('prev_prime', 'next_prime'):
            result = split_places(result)
        elif operation in ('range_prime', 'decompose'):
            result = [split_places(i) for i in result]
    
    # если нужно вернуть развёрнутый ответ
    if explanatory_message.upper() != 'ДА':
        if result is None:
            return 'Нет ответа'
        if operation == 'decompose':  # особый случай для декомпозиции
            return " * ".join(result)
        return str(result).replace(QUOTE_CH, "")

    if operation == 'is_prime':
        return f'Число {number} {result.lower()}'
    elif operation == 'prev_prime':
        if result is None:
            return f'Нет простого числа, которое меньше {number}'
        else:
            return f'Простое число перед {number}: {result}'
    elif operation == 'next_prime':
        return f'Следующее простое число после {number}: {result}'
    elif operation == 'range_prime':
        if result[0] is None:
            return f'Нет простого числа, меньшего {number}. Следующее за ним простое число: {result[1]}'
        else:
            return f'Число {number} находится в диапазоне простых чисел: {str(result).replace(QUOTE_CH, "")}'
    elif operation == 'decompose':
        return f'Результат разложения числа {number} на простые множители: {" * ".join(result)}'
    return 'Неподдерживаемая операция'

@app.route('/', methods=['get', 'post'])
def index():
    form = CoderForm()
    if form.validate_on_submit():
        number              = form.number.data
        operation           = form.operation.data
        split_places_flag   = form.split_places_flag.data
        explanatory_message = form.explanatory_message.data
        
        return redirect(url_for('result', operation=operations_id_dict[operation],
                                          number=number,
                                          split_places_flag=split_places_flag,
                                          explanatory_message=explanatory_message
                                          ))
    if request.method == 'POST':
        number              = request.form.get('number')
        operation           = request.form.get('operation')
        split_places_flag   = request.form.get('split_places_flag')
        explanatory_message = request.form.get('explanatory_message')
        
        #  обработка аргументов POST запроса
        if number is None:
            return 'Значение number не должно быть пустым'
        if operation is None:
            return 'Значение operation не должно быть пустым'
        split_places_flag = split_places_flag is True or split_places_flag == 'True'
        explanatory_message = 'Да' if explanatory_message == 'Да' else 'Нет'

        if operation not in operations_id_dict.values():
            return f'Неподдерживаемая операция {operation}. Поддреживаемые операции: {operations_function_dict.keys()}'
        try:
            number = int(number)
            if number < 1:
                return 'Число должно быть натуральным'
        except ValueError:
            return 'Значение number должно быть натуральным числом'

        result = operations_function_dict[operation](number)
        return format_result(number, operation, result, split_places_flag, explanatory_message)
    
    return render_template('index.html', form=form)

@app.route('/result/operation~<operation>/number~<number>/split_place~<split_places_flag>/explanatory_message~<explanatory_message>')
def result(operation, number, split_places_flag, explanatory_message):
    
    if operation not in operations_id_dict.values():
        abort(404)
    try:
        number = int(number)
        if number < 1:
            return render_template('result.html', result='Число должно быть натуральным')
    except ValueError:
        return render_template('result.html', result='Значение number должно быть натуральным числом')
    
    split_places_flag = split_places_flag == 'True'  # если в переданной строке значение True
    result = operations_function_dict[operation](number)
    return render_template('result.html', result=format_result(number, operation, result, split_places_flag, explanatory_message))
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)