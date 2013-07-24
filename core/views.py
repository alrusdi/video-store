# -*- coding: utf8 -*-
import json

from django.http import HttpResponse
from django.views.generic import ListView


class JsonView(ListView):
    '''
    Единая точка возвращающая Response в формате JSON
    Если необходимо использовать этот генерик без выполнения запрсов к БД
    переопределите метод preprocess и не вызывайте его суперфункцию
    например так:
    def preprocess(self):
        return {'my':'data'}
    '''


    def preprocess(self):
        '''
        Функция для обеспечения возможности фильтрации и преобразования данных
        из QuerySet, возвращаемое значение должно быть корректным для
        стандартного JSON сериализатора
        :return: Окончательный набор данных которые увидит пользователь
        '''
        return self.get_queryset()

    def dispatch(self, request, *args, **kwargs):
        '''
        Сериализует данные в JSON и отдает в браузер
        :param request:
        :param args:
        :param kwargs:
        :return: HttpResponse
        '''
        data = json.dumps(self.preprocess())
        resp = HttpResponse(data, content_type='application/json')
        resp['Expires'] = 'Mon, 1 Jan 2000 01:00:00 GMT'
        resp['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        resp['Pragma'] = 'no-cache'
        return resp
