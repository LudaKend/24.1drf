from rest_framework.serializers import ValidationError
import re

class WrongLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        #print(value)       #для отладки
        #print(self.field)  #для отладки
        tmp_value = dict(value).get(self.field)   #здесь получаем "чистое" содержимое полей, которые будем проверять
        print(type(tmp_value))

        #print(tmp_value)   #для отладки
        temp_list = re.findall(r'(https?://\S+)', str(tmp_value))  #здесь выбираем ссылки из текстовых полей и складываем в список
        print(temp_list)
        for pos in temp_list:
            if 'youtube.com' in pos:
                continue
            else:
                raise ValidationError(f'в поле {self.field} недопустимые ссылки')
