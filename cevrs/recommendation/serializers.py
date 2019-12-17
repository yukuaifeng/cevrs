from .models import  CityRank, ControlLine, Employment, Funds, GradeAll, GradeLine, RankLine, School, Schoolgrade, Strength, StudentNumber, User
from rest_framework import serializers

class GradeAllSerializer(serializers.ModelSerializer):
    """
    GradeAll 表的序列化器，是所有院校的所有录取成绩的表
    """
    class Meta:
        model = GradeAll
        field = '__all__'


class ControlLineSerializer(serializers.ModelSerializer):
    """
    ControlLine 表的序列化器，是湖南省所有省控线的表
    """
    class Meta:
        model = ControlLine
        field = '__all__'


class StudentNumberSerializer(serializers.ModelSerializer):
    """
    StudentNumber 表的序列化器，是近年来考生人数的情况表
    """
    class Meta:
        model = StudentNumber
        field = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    User 表的序列化器，用户表
    """
    class Meta:
        model = User
        field = '__all__'

