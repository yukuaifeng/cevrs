# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class CityRank(models.Model):
    rank = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    clazz = models.CharField(max_length=20, blank=True, null=True)
    grade = models.FloatField(blank=True, null=True)
    top100 = models.IntegerField(blank=True, null=True)
    firstclass = models.IntegerField(blank=True, null=True)
    best = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city_rank'


class ControlLine(models.Model):
    year = models.IntegerField(blank=True, null=True)
    kind = models.CharField(max_length=10, blank=True, null=True)
    clazz = models.CharField(max_length=10, blank=True, null=True)
    ctrl_line = models.IntegerField(blank=True, null=True)
    ctrl_rank = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'control_line'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Employment(models.Model):
    school = models.CharField(max_length=50, blank=True, null=True)
    kind = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    recruit = models.CharField(max_length=50, blank=True, null=True)
    clazz = models.CharField(max_length=50, blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    grade = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employment'


class Funds(models.Model):
    rank = models.IntegerField(blank=True, null=True)
    school = models.CharField(max_length=50, blank=True, null=True)
    fund = models.FloatField(blank=True, null=True)
    all_rank = models.IntegerField(blank=True, null=True)
    stars = models.CharField(max_length=10, blank=True, null=True)
    clazz = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funds'


class GradeAll(models.Model):
    kind = models.CharField(max_length=10, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    school = models.CharField(max_length=50, blank=True, null=True)
    figure = models.IntegerField(blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)
    chinese = models.FloatField(blank=True, null=True)
    math = models.FloatField(blank=True, null=True)
    english = models.FloatField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    clazz = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grade_all'


class GradeLine(models.Model):
    id = models.IntegerField(primary_key=True)
    school = models.CharField(max_length=20, blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    clazz = models.CharField(max_length=8, blank=True, null=True)
    kind = models.CharField(max_length=10, blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grade_line'


class RankLine(models.Model):
    field_school = models.TextField(db_column='\ufeffschool', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    kind = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    grade = models.BigIntegerField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    clazz = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rank_line'


class School(models.Model):
    id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    area = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    if211 = models.CharField(max_length=50, blank=True, null=True)
    if985 = models.CharField(max_length=50, blank=True, null=True)
    funder = models.CharField(max_length=50, blank=True, null=True)
    kind = models.CharField(max_length=50, blank=True, null=True)
    manager = models.CharField(max_length=50, blank=True, null=True)
    managekind = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'school'


class Schoolgrade(models.Model):
    school = models.CharField(max_length=255, blank=True, null=True)
    citygrade = models.FloatField(db_column='cityGrade', blank=True, null=True)  # Field name made lowercase.
    strength = models.FloatField(blank=True, null=True)
    employment = models.FloatField(blank=True, null=True)
    fund = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schoolgrade'


class Strength(models.Model):
    rank = models.IntegerField(blank=True, null=True)
    school = models.CharField(max_length=50, blank=True, null=True)
    grade = models.FloatField(blank=True, null=True)
    star = models.CharField(max_length=10, blank=True, null=True)
    clazz = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'strength'


class StudentNumber(models.Model):
    year = models.IntegerField()
    stu_num = models.IntegerField()
    li_num = models.IntegerField()
    wen_num = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'student_number'


class User(models.Model):
    username = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=128)
    email = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
