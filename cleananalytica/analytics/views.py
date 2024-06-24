# analytics/views.py

from rest_framework import viewsets, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.db.models.functions import TruncDay, TruncMonth
from django.db.models import Avg, Count, Sum,Q,Func
from datetime import datetime
from django.utils.dateparse import parse_date
from rest_framework.decorators import api_view
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np

@api_view(['POST'])
def client_forecast(request):
    try:
        # Получаем данные о количестве клиентов по месяцам
        data = Client.objects.extra({'month': "date_trunc('month', created_at)"}).values('month').annotate(count=Count('id')).order_by('month')
        if not data:
            return Response({"error": "No data available for forecasting"}, status=status.HTTP_400_BAD_REQUEST)

        df = pd.DataFrame(data)
        df['month'] = pd.to_datetime(df['month'])
        df.set_index('month', inplace=True)
        df = df.asfreq('MS')  # Добавляем информацию о частоте данных
        print("DataFrame:\n", df)  # Вывод данных для проверки

        # Прогнозируем данные на следующий месяц
        model = ARIMA(df['count'], order=(5, 1, 0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=1)
        next_month_forecast = round(forecast[0])
        print("Forecast:\n", next_month_forecast)  # Вывод прогноза для проверки

        return Response({"forecast": next_month_forecast}, status=status.HTTP_200_OK)
    except Exception as e:
        print("Error:", str(e))  # Вывод ошибки для проверки
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def client_dynamics(request):
    try:
        data = Client.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
        report = [{'month': item['month'].strftime('%Y-%m'), 'count': item['count']} for item in data]
        return Response(report, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def order_dynamics(request):
    try:
        data = Order.objects.annotate(date=TruncDay('created_at')).values('date').annotate(count=Count('id')).order_by('date')
        report = [{'date': item['date'].strftime('%Y-%m-%d'), 'count': item['count']} for item in data]
        return Response(report, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def save_report(request):
    try:
        report_name = request.data.get('name')
        report_type = request.data.get('type')
        report_data_type = request.data.get('data_type')
        report_data = request.data.get('data')
        SavedReport.objects.create(name=report_name, type=report_type,data_type=report_data_type, data=report_data)
        return Response({"message": "Report saved successfully!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_reports(request):
    try:
        reports = SavedReport.objects.all()
        serializer = SavedReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['GET'])    
def get_managers(request):
    try:
        manager = Employee.objects.filter(position__name="Менеджер")
        serializer = EmployeeSerializer(manager, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 2)'

@api_view(['POST'])
def generate_report(request, data_type):
    try:
        report_type = request.data.get('data_type')
        
        if data_type == 'order':
            if report_type == 'summary':
                data = Order.objects.select_related('client', 'status', 'manager').all()
                report = [
                    {
                        'id': order.id,
                        'client_first_name': order.client.first_name,
                        'client_last_name': order.client.last_name,
                        'client_middle_name': order.client.middle_name,
                        'status_name': order.status.name,
                        'manager_first_name': order.manager.first_name,
                        'manager_last_name': order.manager.last_name,
                        'total_cost': order.total_cost,
                        'comments': order.comments
                    }
                    for order in data
                ]
            elif report_type == 'daily_dynamics':
                
                data = Order.objects.annotate(date=TruncDay('created_at')).values('date').annotate(count=Count('id')).order_by('date')
                report = [{'date': item['date'].strftime('%Y-%m-%d'), 'count': item['count']} for item in data]
                
            elif report_type == 'monthly_dynamics':
                data = Order.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
                report = [{'month': item['month'].strftime('%B %Y'), 'count': item['count']} for item in data]
                print('Generated report:', report)
            elif report_type == 'average_cost':
                data = Order.objects.aggregate(avg_cost=Avg('total_cost'))
                report = [{'avg_cost': data['avg_cost']}]
                print('Generated:', report)
            elif report_type == 'success_comparison':
                data = Order.objects.values('status__name').annotate(count=Count('id')).order_by('status__name')
                report = [{'status': item['status__name'], 'count': item['count']} for item in data]

        elif data_type == 'client':
            
            if report_type == 'monthly_dynamics':
                data = Client.objects.extra({'month': "to_char(created_at, 'YYYY-MM')"}).values('month').annotate(count=Count('id')).order_by('month')
                report = [{'month': item['month'], 'count': item['count']} for item in data]
            elif report_type == 'summary':
                data = Client.objects.all()
                report = [
                    {
                        'id': client.id,
                        'first_name': client.first_name,
                        'last_name': client.last_name,
                        'middle_name': client.middle_name,
                        'phone_number': client.phone_number
                    }
                    for client in data
                ]
            elif report_type == 'top_clients':
                data = Client.objects.annotate(order_count=Count('order')).filter(order_count__gt=0).order_by('-order_count')[:10]
                report = [
                    {
                        'id': client.id,
                        'first_name': client.first_name,
                        'last_name': client.last_name,
                        'middle_name': client.middle_name,
                        'phone_number': client.phone_number,
                        'order_count': client.order_count
                    }
                    for client in data
                ]

        elif data_type == 'employee':
            if report_type == 'summary':
                data = Employee.objects.select_related('position', 'team').all()
                report = [
                    {
                        'id': employee.id,
                        'first_name': employee.first_name,
                        'last_name': employee.last_name,
                        'middle_name': employee.middle_name,
                        'position': employee.position.name,
                        'team': employee.team.name,
                        'phone_number': employee.phone_number
                    }
                    for employee in data
                ]
            elif report_type == 'ratings_dynamics':
                data = EmployeeRating.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(avg_rating=Avg('rating')).order_by('month')
                report = [{'month': item['month'], 'avg_rating': item['avg_rating']} for item in data]
            elif report_type == 'manager_report':
                manager_id = request.data.get('manager_id')
                data = Order.objects.filter(manager_id=manager_id).aggregate(
                    total_orders=Count('id'),
                    successful_orders=Count('id', filter=Q(status__name='Выполнен')),
                    total_income=Sum('total_cost')
                )
                report = data

        elif data_type == 'service':
            if report_type == 'summary':
                data = Service.objects.all()
                report = [
                    {
                        'id': service.id,
                        'name': service.name,
                        'description': service.description,
                        'base_cost': service.base_cost
                    }
                    for service in data
                ]
            elif report_type == 'frequency':
                data = Service.objects.annotate(
                count=Count('objectservice__id')
                ).order_by('-count').values('name', 'count')
                report = [{'name': item['name'], 'count': item['count']} for item in data]
            elif report_type == 'cost_comparison':
                data = Service.objects.values('name').annotate(avg_cost=Avg('base_cost')).order_by('-avg_cost')
                report = [{'name': item['name'], 'avg_cost': item['avg_cost']} for item in data]

        elif data_type == 'object':
            if report_type == 'summary':
                data = Object.objects.select_related('type').all()
                report = [
                    {
                        'id': obj.id,
                        'type': obj.type.name,
                        'address': obj.address,
                        'area': obj.area
                    }
                    for obj in data
                ]
            elif report_type == 'most_requested':
                
                data = ObjectService.objects.values('object__type__name', 'object__address') \
                    .annotate(count=Count('id')) \
                    .order_by('-count')
                report = [{'type': item['object__type__name'], 'address': item['object__address'], 'count': item['count']} for item in data]
            else:
                data = Object.objects.all()
                report = [{'id': obj.id, 'type': obj.type.name, 'address': obj.address, 'area': obj.area} for obj in data]

        elif data_type == 'team':
            if report_type == 'summary':
                data = Team.objects.all()
                report = [
                    {
                        'id': team.id,
                        'name': team.name
                    }
                    for team in data
                ]
            elif report_type == 'efficiency':
                 
                data = Team.objects.annotate(
                    total_orders=Count('employee__order'),
                    avg_cost=Avg('employee__order__total_cost')
                ).order_by('-total_orders')

                report = [
                    {
                        'name': team.name,
                        'total_orders': team.total_orders,
                        'avg_cost': team.avg_cost
                    }
                    for team in data
                ]

        elif data_type == 'cleanerskill':
            if report_type == 'summary':
                data = Skill.objects.all()
                report = [
                    {
                        'id': skill.id,
                        'name': skill.name
                    }
                    for skill in data
                ]
            elif report_type == 'comparison':
                data = Skill.objects.annotate(cleaner_count=Count('cleaner')).order_by('-cleaner_count')
                report = [{'name': skill.name, 'cleaner_count': skill.cleaner_count} for skill in data]

        return Response(report, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)        

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class CleanerViewSet(viewsets.ModelViewSet):
    queryset = Cleaner.objects.all()
    serializer_class = CleanerSerializer

class CleanerSkillViewSet(viewsets.ModelViewSet):
    queryset = CleanerSkill.objects.all()
    serializer_class = CleanerSkillSerializer

class TimeTypeViewSet(viewsets.ModelViewSet):
    queryset = TimeType.objects.all()
    serializer_class = TimeTypeSerializer

class WorkScheduleViewSet(viewsets.ModelViewSet):
    queryset = WorkSchedule.objects.all()
    serializer_class = WorkScheduleSerializer

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientsReportView(APIView):
    def get(self, request):
        try:
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')

            clients = Client.objects.filter(
                created_at__range=[start_date, end_date]
            ).annotate(
                total_orders=Count('order'),
                total_spent=Sum('order__total_cost')
            ).values('first_name', 'last_name', 'middle_name', 'phone_number', 'total_orders', 'total_spent')
            
            return Response(clients, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ObjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ObjectType.objects.all()
    serializer_class = ObjectTypeSerializer

class ObjectViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

class RoomFormViewSet(viewsets.ModelViewSet):
    queryset = RoomForm.objects.all()
    serializer_class = RoomFormSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class SurfaceViewSet(viewsets.ModelViewSet):
    queryset = Surface.objects.all()
    serializer_class = SurfaceSerializer

class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer

class ServiceSurfaceViewSet(viewsets.ModelViewSet):
    queryset = ServiceSurface.objects.all()
    serializer_class = ServiceSurfaceSerializer

class ServiceOperationViewSet(viewsets.ModelViewSet):
    queryset = ServiceOperation.objects.all()
    serializer_class = ServiceOperationSerializer

class ServiceRoomViewSet(viewsets.ModelViewSet):
    queryset = ServiceRoom.objects.all()
    serializer_class = ServiceRoomSerializer

class ServiceZoneViewSet(viewsets.ModelViewSet):
    queryset = ServiceZone.objects.all()
    serializer_class = ServiceZoneSerializer

class ServicePackageViewSet(viewsets.ModelViewSet):
    queryset = ServicePackage.objects.all()
    serializer_class = ServicePackageSerializer

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

class FloorServiceViewSet(viewsets.ModelViewSet):
    queryset = FloorService.objects.all()
    serializer_class = FloorServiceSerializer

class ObjectServiceViewSet(viewsets.ModelViewSet):
    queryset = ObjectService.objects.all()
    serializer_class = ObjectServiceSerializer

class EmployeeRatingViewSet(viewsets.ModelViewSet):
    queryset = EmployeeRating.objects.all()
    serializer_class = EmployeeRatingSerializer

class CleanerOrderAssignmentViewSet(viewsets.ModelViewSet):
    queryset = CleanerOrderAssignment.objects.all()
    serializer_class = CleanerOrderAssignmentSerializer

class ReplacementCleanerOrderAssignmentViewSet(viewsets.ModelViewSet):
    queryset = ReplacementCleanerOrderAssignment.objects.all()
    serializer_class = ReplacementCleanerOrderAssignmentSerializer

class ReportView(views.APIView):
     def post(self, request):
        data_type = request.data.get('data_type')
        if not data_type:
            return Response({"error": "Missing 'data_type' field"}, status=status.HTTP_400_BAD_REQUEST)

        data = None
        serializer = None

        if data_type == 'skill':
            data = Skill.objects.all()
            serializer = SkillSerializer(data, many=True)
        elif data_type == 'cleaner':
            data = Cleaner.objects.all()
            serializer = CleanerSerializer(data, many=True)
        elif data_type == 'order':
            data = Order.objects.all()
            serializer = OrderSerializer(data, many=True)
        else:
            return Response({"error": "Invalid data type"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

class OrdersDynamicsView(APIView):
    def get(self, request, period='day'):
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                if period == 'day':
                    data = Order.objects.filter(created_at__range=(start_date, end_date)).annotate(date=TruncDay('created_at')).values('date').annotate(count=Count('id')).order_by('date')
                elif period == 'month':
                    data = Order.objects.filter(created_at__range=(start_date, end_date)).annotate(date=TruncMonth('created_at')).values('date').annotate(count=Count('id')).order_by('date')
            else:
                if period == 'day':
                    data = Order.objects.annotate(date=TruncDay('created_at')).values('date').annotate(count=Count('id')).order_by('date')
                elif period == 'month':
                    data = Order.objects.annotate(date=TruncMonth('created_at')).values('date').annotate(count=Count('id')).order_by('date')
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NewClientsDynamicsView(APIView):
    def get(self, request):
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                data = Client.objects.filter(created_at__range=(start_date, end_date)).annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
            else:
                data = Client.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AverageOrderCostView(APIView):
    def get(self, request):
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                data = Order.objects.filter(created_at__range=(start_date, end_date)).aggregate(avg_cost=Avg('total_cost'))
            else:
                data = Order.objects.aggregate(avg_cost=Avg('total_cost'))
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PositiveRatingsDynamicsView(APIView):
    def get(self, request):
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                data = EmployeeRating.objects.filter(created_at__range=(start_date, end_date), rating__gte=4).annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
            else:
                data = EmployeeRating.objects.filter(rating__gte=4).annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')). order_by('month')
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ManagerMonthlyReportView(APIView):
    def get(self, request, manager_id):
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                data = Order.objects.filter(manager_id=manager_id, created_at__range=(start_date, end_date)).aggregate(
                    total_orders=Count('id'),
                    successful_orders=Count('id', filter=models.Q(status__name='Выполнен')),
                    total_income=Sum('total_cost')
                )
            else:
                data = Order.objects.filter(manager_id=manager_id).aggregate(
                    total_orders=Count('id'),
                    successful_orders=Count('id', filter=models.Q(status__name='Выполнен')),
                    total_income=Sum('total_cost')
                )
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class OrderDetailView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            data = {
                'client': {
                    'first_name': order.client.first_name,
                    'last_name': order.client.last_name,
                    'middle_name': order.client.middle_name,
                    'phone_number': order.client.phone_number,
                },
                'status': order.status.name,
                'created_at': order.created_at,
                'start_date': order.start_date,
                'end_date': order.end_date,
                'manager': {
                    'first_name': order.manager.first_name,
                    'last_name': order.manager.last_name,
                    'middle_name': order.manager.middle_name,
                    'position': order.manager.position.name,
                },
                'comments': order.comments,
                'total_cost': order.total_cost,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class OrdersReportView(APIView):
    def post(self, request):
        try:
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            orders = Order.objects.filter(created_at__range=[start_date, end_date])
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderReportView(APIView):
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            orders = Order.objects.filter(created_at__range=(start_date, end_date))
        else:
            orders = Order.objects.all()

        data_type = request.data.get('data_type')
        
        if data_type == 'summary':
            serializer = OrderSerializer(orders, many=True)
        elif data_type == 'daily_dynamics':
            data = orders.annotate(date=TruncDay('created_at')).values('date').annotate(count=Count('id')).order_by('date')
            return Response(data, status=status.HTTP_200_OK)
        elif data_type == 'monthly_dynamics':
            data = orders.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
            return Response(data, status=status.HTTP_200_OK)
        elif data_type == 'average_cost':
            data = orders.aggregate(avg_cost=Avg('total_cost'))
            return Response(data, status=status.HTTP_200_OK)
        elif data_type == 'success_comparison':
            success = orders.filter(status__name='Новый').count()
            failure = orders.exclude(status__name='Выполнен').count()
            data = {'successful': success, 'unsuccessful': failure}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid data type"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ClientReportView(APIView):
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            clients = Client.objects.filter(created_at__range=(start_date, end_date))
        else:
            clients = Client.objects.all()

        data_type = request.data.get('data_type')
        
        if data_type == 'monthly_dynamics':
            data = clients.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
            return Response(data, status=status.HTTP_200_OK)
        elif data_type == 'summary':
            serializer = ClientSerializer(clients, many=True)
        elif data_type == 'top_clients':
            data = Client.objects.annotate(order_count=Count('order')).order_by('-order_count')[:10]
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid data type"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)        

class EmployeeReportView(APIView):
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            employees = Employee.objects.filter(order__created_at__range=(start_date, end_date)).distinct()
        else:
            employees = Employee.objects.all()

        data_type = request.data.get('data_type')
        
        if data_type == 'summary':
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif data_type == 'ratings_dynamics':
            ratings = EmployeeRating.objects.filter(created_at__range=(start_date, end_date)).annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
            return Response(ratings, status=status.HTTP_200_OK)
        elif data_type == 'manager_report':
            manager_id = request.data.get('manager_id')
            if not manager_id:
                return Response({"error": "manager_id is required for this report"}, status=status.HTTP_400_BAD_REQUEST)
            
            current_month = datetime.datetime.now().month
            report = Order.objects.filter(manager_id=manager_id, created_at__month=current_month).aggregate(
                total_orders=Count('id'),
                successful_orders=Count('id', filter=Q(status__name='Выполнен')),
                total_income=Sum('total_cost')
            )
            return Response(report, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid data type"}, status=status.HTTP_400_BAD_REQUEST)
        
class ServiceReportView(APIView):
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            services = Service.objects.filter(order__created_at__range=(start_date, end_date)).distinct()
        else:
            services = Service.objects.all()

        data_type = request.data.get('data_type')
        
        if data_type == 'summary':
            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif data_type == 'frequency':
            data = services.annotate(order_count=Count('order')).order_by('-order_count')
            return Response(data, status=status.HTTP_200_OK)
        elif data_type == 'cost_comparison':
            data = {
                'operations': ServiceOperation.objects.values('operation__name').annotate(avg_cost=Avg('cost')).order_by('-avg_cost'),
                'surfaces': ServiceSurface.objects.values('surface__name').annotate(avg_cost=Avg('cost')).order_by('-avg_cost'),
                'rooms': ServiceRoom.objects.values('room__type__name').annotate(avg_cost=Avg('cost')).order_by('-avg_cost'),
                'zones': ServiceZone.objects.values('zone__name').annotate(avg_cost=Avg('cost')).order_by('-avg_cost')
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid data type"}, status=status.HTTP_400_BAD_REQUEST)

class ObjectReportView(APIView):
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            objects = Object.objects.filter(order__created_at__range=(start_date, end_date)).distinct()
        else:
            objects = Object.objects.all()

        data_type = request.data.get('data_type')
        
        if data_type == 'summary':
            serializer = ObjectSerializer(objects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif data_type == 'most_requested':
            data = objects.annotate(order_count=Count('order')).order_by('-order_count')[:10]
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid data type"}, status=status.HTTP_400_BAD_REQUEST)

class TeamReportView(APIView):
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            teams = Team.objects.filter(order__created_at__range=(start_date, end_date)).distinct()
        else:
            teams = Team.objects.all()

        data_type = request.data.get('data_type')
        
        if data_type == 'summary':
            serializer = TeamSerializer(teams, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif data_type == 'efficiency':
            data = teams.annotate(
                total_orders=Count('order'),
                avg_cost=Avg('order__total_cost')
            ).order_by('-total_orders')
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid data type"}, status=status.HTTP_400_BAD_REQUEST)

class CleanerSkillReportView(APIView):
    def post(self, request):
        skills = Skill.objects.all()

        data_type = request.data.get('data_type')
        
        if data_type == 'summary':
            serializer = SkillSerializer(skills, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif data_type == 'comparison':
            data = skills.annotate(cleaner_count=Count('cleanerskill')).order_by('-cleaner_count')
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid data type"}, status=status.HTTP_400_BAD_REQUEST)                                