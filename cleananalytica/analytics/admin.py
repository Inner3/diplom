# analytics/admin.py

from django.contrib import admin
from .models import (
    Skill, Cleaner, CleanerSkill, TimeType, WorkSchedule,
    Position, Team, Employee, Client, Status, Order,
    Object, ObjectType, Room, RoomType, RoomForm, Zone,
    Service, Surface, Operation, ServiceSurface,
    ServiceOperation, ServiceRoom, ServiceZone, ServicePackage,
    Building, Floor, FloorService, ObjectService, EmployeeRating,
    CleanerOrderAssignment, ReplacementCleanerOrderAssignment
)

admin.site.register(Skill)
admin.site.register(Cleaner)
admin.site.register(CleanerSkill)
admin.site.register(TimeType)
admin.site.register(WorkSchedule)
admin.site.register(Position)
admin.site.register(Team)
admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Status)
admin.site.register(Order)
admin.site.register(Object)
admin.site.register(ObjectType)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(RoomForm)
admin.site.register(Zone)
admin.site.register(Service)
admin.site.register(Surface)
admin.site.register(Operation)
admin.site.register(ServiceSurface)
admin.site.register(ServiceOperation)
admin.site.register(ServiceRoom)
admin.site.register(ServiceZone)
admin.site.register(ServicePackage)
admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(FloorService)
admin.site.register(ObjectService)
admin.site.register(EmployeeRating)
admin.site.register(CleanerOrderAssignment)
admin.site.register(ReplacementCleanerOrderAssignment)

