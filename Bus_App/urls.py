from django.urls import path
from Bus_App import views
urlpatterns = [
    path('',views.home_page,name="home_page"),
    path('stud_login_page/',views.stud_login_page,name="stud_login_page"),
    path('stud_dashboard/',views.stud_dashboard,name="stud_dashboard"),
    path('stud_login_fn/',views.stud_login_fn,name="stud_login_fn"),
    path('display_stud_bus/',views.display_stud_bus,name="display_stud_bus"),
    path('display_staff_bus/',views.display_staff_bus,name="display_staff_bus"),
    path('stud_profile/',views.stud_profile,name="stud_profile"),
    path('staff_login_page/',views.staff_login_page,name="staff_login_page"),
    path('staff_dashboard/',views.staff_dashboard,name="staff_dashboard"),
    path('staff_profile/',views.staff_profile,name="staff_profile"),
    path('staff_login_fn/',views.staff_login_fn,name="staff_login_fn"),
    path('stud_logout_fn/',views.stud_logout_fn,name="stud_logout_fn"),
    path('staff_logout_fn/',views.staff_logout_fn,name="staff_logout_fn"),

    path('scan_qr/',views.teacher_scan_qr,name='scan_qr'),
    path('show_qr/',views.show_qr,name='show_qr'),
    path("student/qr",views.generate_qr,name="student_qr"),
    path("scan-result/",views.scan_result,name="scan_result"),
]

