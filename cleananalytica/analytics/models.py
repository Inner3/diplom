# analytics/models.py

from django.db import models
import datetime

class Skill(models.Model):  # Навык
    name = models.CharField(max_length=100)

class Team(models.Model):  # Команда
    name = models.CharField(max_length=100)

class Cleaner(models.Model):  # Клинер
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, through='CleanerSkill')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class CleanerSkill(models.Model):  # Навык клинера
    cleaner = models.ForeignKey(Cleaner, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

class TimeType(models.Model):  # Тип времени
    name = models.CharField(max_length=100)

class WorkSchedule(models.Model):  # График работы
    cleaner = models.ForeignKey(Cleaner, on_delete=models.CASCADE)
    date = models.DateField()
    time_type = models.ForeignKey(TimeType, on_delete=models.CASCADE)

class Position(models.Model):  # Должность
    name = models.CharField(max_length=100)



class Employee(models.Model):  # Сотрудник
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='photos/')
    passport_details = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class Client(models.Model):  # Клиент
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)  # Добавлено поле

class Status(models.Model):  # Статус
    name = models.CharField(max_length=100)

class Order(models.Model):  # Заявка
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE)
    comments = models.TextField()
    total_cost = models.FloatField()

class ObjectType(models.Model):  # Тип объекта
    name = models.CharField(max_length=100) 

class Object(models.Model):  # Объект
    type = models.ForeignKey(ObjectType, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    area = models.FloatField()

class RoomType(models.Model):  # Тип помещения
    name = models.CharField(max_length=100)

class RoomForm(models.Model):  # Форма помещения
    name = models.CharField(max_length=100)

class Room(models.Model):  # Помещение
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    form = models.ForeignKey(RoomForm, on_delete=models.CASCADE)
    area = models.FloatField()
    height = models.FloatField()
    comment = models.TextField()

class Zone(models.Model):  # Зона
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    area = models.FloatField()

class Service(models.Model):  # Услуга
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_cost = models.FloatField()

class Surface(models.Model):  # Поверхность
    name = models.CharField(max_length=100)

class Operation(models.Model):  # Операция
    name = models.CharField(max_length=100)

class ServiceSurface(models.Model):  # Услуга поверхности
    surface = models.ForeignKey(Surface, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    cost = models.FloatField()

class ServiceOperation(models.Model):  # Услуга операции
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    cost = models.FloatField()

class ServiceRoom(models.Model):  # Услуга помещения
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    cost = models.FloatField()

class ServiceZone(models.Model):  # Услуга зоны
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    cost = models.FloatField()

class ServicePackage(models.Model):  # Комплекс услуг
    name = models.CharField(max_length=100)
    services = models.ManyToManyField(Service)

class Building(models.Model):  # Строение
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    intercom = models.CharField(max_length=100)
    number_of_floors = models.IntegerField()

class Floor(models.Model):  # Этаж
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    number = models.IntegerField()
    area = models.FloatField()

class FloorService(models.Model):  # Услуга этажа
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    cost = models.FloatField()
    comment = models.TextField()

class ObjectService(models.Model):  # Услуга объекта
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    cost = models.FloatField()
    comment = models.TextField()

class EmployeeRating(models.Model):  # Рейтинг сотрудника
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class CleanerOrderAssignment(models.Model):  # Клинер на заявку
    cleaner = models.ForeignKey(Cleaner, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    wage = models.FloatField()

class ReplacementCleanerOrderAssignment(models.Model):  # Резервный клинер на заявку
    cleaner = models.ForeignKey(Cleaner, on_delete=models.CASCADE, related_name='replacement_cleaner')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    wage = models.FloatField()
    comment = models.TextField()

class SavedReport(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    data_type = models.CharField(max_length=50)
    data = models.JSONField()

    def __str__(self):
        return self.name
    
