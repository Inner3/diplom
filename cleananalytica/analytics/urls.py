# analytics/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'skills', SkillViewSet)
router.register(r'cleaners', CleanerViewSet)
router.register(r'cleaner-skills', CleanerSkillViewSet)
router.register(r'time-types', TimeTypeViewSet)
router.register(r'work-schedules', WorkScheduleViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'statuses', StatusViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'object-types', ObjectTypeViewSet)
router.register(r'objects', ObjectViewSet)
router.register(r'room-types', RoomTypeViewSet)
router.register(r'room-forms', RoomFormViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'zones', ZoneViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'surfaces', SurfaceViewSet)
router.register(r'operations', OperationViewSet)
router.register(r'service-surfaces', ServiceSurfaceViewSet)
router.register(r'service-operations', ServiceOperationViewSet)
router.register(r'service-rooms', ServiceRoomViewSet)
router.register(r'service-zones', ServiceZoneViewSet)
router.register(r'service-packages', ServicePackageViewSet)
router.register(r'buildings', BuildingViewSet)
router.register(r'floors', FloorViewSet)
router.register(r'floor-services', FloorServiceViewSet)
router.register(r'object-services', ObjectServiceViewSet)
router.register(r'employee-ratings', EmployeeRatingViewSet)
router.register(r'cleaner-order-assignments', CleanerOrderAssignmentViewSet)
router.register(r'replacement-cleaner-order-assignments', ReplacementCleanerOrderAssignmentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('report/', ReportView.as_view(), name='report'),
    path('report/orders-dynamics/<str:period>/', OrdersDynamicsView.as_view(), name='orders-dynamics'),
    path('report/new-clients-dynamics/', NewClientsDynamicsView.as_view(), name='new-clients-dynamics'),
    path('report/average-order-cost/', AverageOrderCostView.as_view(), name='average-order-cost'),
    path('report/positive-ratings-dynamics/', PositiveRatingsDynamicsView.as_view(), name='positive-ratings-dynamics'),
    path('report/manager-monthly-report/<int:manager_id>/', ManagerMonthlyReportView.as_view(), name='manager-monthly-report'),
    path('report/order-detail/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('api/report/clients/', ClientsReportView.as_view(), name='clients-report'),
    path('api/OrdersReportView/',OrdersReportView.as_view(),name='orders-report'),
    # path('report/order/', OrderReportView.as_view(), name='order-report'),
    # path('report/client/', ClientReportView.as_view(), name='client-report'),
    # path('report/employee/', EmployeeReportView.as_view(), name='employee-report'),
    # path('report/service/', ServiceReportView.as_view(), name='service-report'),
    # path('report/object/', ObjectReportView.as_view(), name='object-report'),
    # path('report/team/', TeamReportView.as_view(), name='team-report'),
    # path('report/cleanerskill/', CleanerSkillReportView.as_view(), name='cleanerskill-report'),
    path('save-report/', save_report, name='save-report'),
    path('managers/', get_managers, name='get_managers'),
    path('report/<str:data_type>/', generate_report, name='generate_report'),
    path('reports/', get_reports, name='get_reports'),
    path('client-dynamics/',client_dynamics,name='client_dynamics'),
    path('order-dynamics/',order_dynamics),
    path('client-forecast/', client_forecast, name='client-forecast'),
    
]
