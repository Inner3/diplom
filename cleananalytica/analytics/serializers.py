# analytics/serializers.py

from rest_framework import serializers
from .models import *

class SavedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedReport
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class CleanerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cleaner
        fields = '__all__'

class CleanerSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleanerSkill
        fields = '__all__'

class TimeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeType
        fields = '__all__'

class WorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ObjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectType
        fields = '__all__'

class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'

class RoomFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomForm
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class SurfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surface
        fields = '__all__'

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'

class ServiceSurfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSurface
        fields = '__all__'

class ServiceOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOperation
        fields = '__all__'

class ServiceRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRoom
        fields = '__all__'

class ServiceZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceZone
        fields = '__all__'

class ServicePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePackage
        fields = '__all__'

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'

class FloorServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorService
        fields = '__all__'

class ObjectServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectService
        fields = '__all__'

class EmployeeRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRating
        fields = '__all__'

class CleanerOrderAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleanerOrderAssignment
        fields = '__all__'

class ReplacementCleanerOrderAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplacementCleanerOrderAssignment
        fields = '__all__'
