from django.http import HttpResponse
from .models import GradeAll, ControlLine, StudentNumber, User
from rest_framework import viewsets
from .serializers import GradeAllSerializer, ControlLineSerializer, StudentNumberSerializer, UserSerializer
from recommendation.utils import choose
import json


# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. Success get in views")
    if request.method == 'POST':
        score = int(request.POST.get('score'))
        rank = int(request.POST.get('rank'))
        radio = request.POST.get('radio')
        first_value = request.POST.get('firstValue')
        second_value = request.POST.get('secondValue')
        third_value = request.POST.get('thirdValue')
        fourth_value = request.POST.get('fourthValue')
        risk_number = int(request.POST.get('riskNum'))
        surely_number = int(request.POST.get('surelyNum'))
        def_number = int(request.POST.get('defiNum'))
        print(score, rank, radio, first_value, second_value, third_value, fourth_value,
              risk_number, surely_number, def_number)
        riskly_results, surely_results, definite_results = choose.choose_school(rank, radio, first_value, second_value,
                                                                                third_value, fourth_value, risk_number,
                                                                                surely_number, def_number)
        result_keys = ['school', 'rate', 'clazz', 'ranks', 'school_grades', 'ctrl_grades', 'kind']
        result_list = []
        for risk_result in riskly_results:
            new_risk_result = risk_result + ('冲',)
            risk_results_dict = {i: new_risk_result[result_keys.index(i)] for i in result_keys}
            result_list.append(risk_results_dict)

        for surely_result in surely_results:
            new_surely_result = surely_result + ('稳',)
            surely_results_dict = {i: new_surely_result[result_keys.index(i)] for i in result_keys}
            result_list.append(surely_results_dict)

        for definite_result in definite_results:
            new_definite_result = definite_result + ('保',)
            definite_results_dict = {i: new_definite_result[result_keys.index(i)] for i in result_keys}
            result_list.append(definite_results_dict)
        results = {
            'data': result_list,
            'message': 'success'
        }
        print(results)
        return HttpResponse(json.dumps(results), content_type="application/json,charset=utf-8")
