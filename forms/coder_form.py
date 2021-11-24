from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, BooleanField, RadioField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class CoderForm(FlaskForm):
    # натуральное число т.е. целое число > 1
    number = IntegerField("Число для анализа:", validators=[DataRequired(), NumberRange(1)])
    
    # набор операций
    operation = SelectField(
        'Выберите операцию:',
        coerce=int,
        choices=[
            (0, 'Является ли число простым?'),
            (1, 'Найти предыдущее простое число'),
            (2, 'Найти следующее простое число'),
            (3, 'Найти промежуток простых чисел, в котором находится число'),
            (4, 'Разложить число на простые множители'),
        ]
    )
    
    split_places_flag = BooleanField('Разделять числа в ответе по разрядам:', default=True)
    explanatory_message = RadioField('Развёрнутый ответ:', choices=['Да', 'Нет'], default='Да')
    
    # submit кнопка
    submit = SubmitField("Рассчитать")