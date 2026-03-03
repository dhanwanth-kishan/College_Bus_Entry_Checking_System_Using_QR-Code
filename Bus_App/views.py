from django.shortcuts import render,redirect
from Bus_App.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
import qrcode,base64
from io import BytesIO
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
import datetime as dt
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib import messages



def home_page(request):
    return render(request,'home.html')

def stud_login_page(request):
    return render(request,'stud-login.html')

def stud_profile(request): 
    student=StudentData.objects.get(user=request.user)
    return render(request,'stud-profile.html',{'student':student})

def stud_login_fn(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')

        user_exists = User.objects.filter(username=u_name).exists()
        
        if not user_exists:
            messages.error(request,'invalid credentials')
            return render(request, 'stud-login.html', {'u_error': 'Username not found'})

        user = authenticate(request, username=u_name, password=p_word)
        
        if user is not None:
            login(request, user)
            staff = StudentData.objects.get(user=user)
            request.session['name'] = staff.Name
            messages.success(request,f'Login Success, Welcome back..{request.session['name']}')
            return redirect('stud_dashboard')
        else:
            messages.error(request,'invalid credentials')
            return render(request, 'stud-login.html', {'p_error': 'Invalid password!', 'old_user': u_name})
            
    return render(request, 'stud-login.html')

@never_cache
@login_required(login_url='stud_login_page')
def stud_dashboard(request):
    student=StudentData.objects.get(user=request.user)
    return render(request,'student-dashboard.html',{'student':student})

def staff_login_page(request):
    return render(request,'staff-login.html')


@never_cache
@login_required(login_url='staff_login_page')
def staff_dashboard(request):
    staff = StaffData.objects.get(user=request.user)
    return render(request,'staff-dashboard.html',{'staff':staff})

def staff_profile(request):
    staff=StaffData.objects.get(user=request.user)
    return render(request,'staff-profile.html',{'staff':staff})

def stud_logout_fn(request):
    logout(request)
    return redirect('home_page')



def staff_login_fn(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')

        user_exists = User.objects.filter(username=u_name).exists()
        
        if not user_exists:
            messages.error(request,'invalid credentials')
            return render(request, 'staff-login.html', {'u_error': 'Username not found'})

        
        user = authenticate(request, username=u_name, password=p_word)
        
        if user is not None:
            login(request, user)
            staff = StaffData.objects.get(user=user)
            request.session['name'] = staff.Name
            messages.success(request,f'Login Success, Welcome back..{request.session['name']}')
            return redirect('staff_dashboard')
        else:
            messages.error(request,'invalid credentials')
            return render(request, 'staff-login.html', {'p_error': 'Invalid password', 'old_user': u_name})
            
    return render(request, 'staff-login.html')  

def display_stud_bus(request):
    student=StudentData.objects.get(user=request.user).Bus_Number
    student_data=StudentData.objects.get(user=request.user)
    busdata=BusData.objects.filter(id=student)
    return render(request,'display-stud-bus.html',{'busdata':busdata,'student':student,'student_data':student_data})


def display_staff_bus(request):
    staff=StaffData.objects.get(user=request.user).Bus_Number
    staff_data=StaffData.objects.get(user=request.user)
    busdata=BusData.objects.filter(id=staff)
    return render(request,'display-staff-bus.html',{'busdata':busdata,'staff':staff,'staff_data':staff_data})

@never_cache
@login_required(login_url='staff_login_page')
def teacher_scan_qr(request):
    staff=StaffData.objects.get(user=request.user)
    staff_data=StaffData.objects.get(user=request.user)
    return render(request,'scan-qr.html',{'staff':staff,'staff_data':staff_data})

@never_cache
@login_required(login_url='stud_login_page')
def show_qr(request):
    student = StudentData.objects.get(user=request.user)

    qr = qrcode.make(student.Stud_id)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'show-qr.html', {
        'student': student,
        'qr_code': img_str
    })


def scan_result(request):
    student_id = request.GET.get('student_id')

    if not student_id:
        return JsonResponse({
            "status": "error",
            "message": "Invalid QR Data"
        })
    try:
        student = StudentData.objects.get(Stud_id=student_id)
    except StudentData.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Invalid QR Code"
        })
    try:
        staff = StaffData.objects.get(user=request.user)
    except StaffData.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Staff not found"
        })

    if str(student.Bus_Number).strip() != str(staff.Bus_Number).strip():
        return JsonResponse({
            "status": "error",
            "message": "Student does not belong to your bus"
        })

    today = dt.datetime.now().date()

    if BusEntry.objects.filter(student=student, date=today).exists():
        return JsonResponse({
            "status": "error",
            "message": "Duplicate Entry - Already Scanned Today"
        })

    BusEntry.objects.create(
        student=student,
        staff=staff
    )

    return JsonResponse({
        "status": "success",
        "message": "Entry Allowed",
        "student": {
            "name": student.Name,
            "id": student.Stud_id,
            "bus": student.Bus_Number,
            "department": student.Department
        }
    })
def view_qr(request):
    try:
        student = StudentData.objects.get(user=request.user)
    except StudentData.DoesNotExist:
        return redirect('scan_qr')  

    return render(request, 'show-qr.html', {'student': student})

def staff_logout_fn(request):
    logout(request)
    return redirect('home_page')

def get_in_touch(request):
    if request.method=="POST":
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        obj3=GetINTouch(Name=name,Number=phone,Email=email,Subject=subject,Message=message)
        obj3.save()
    
        return redirect(home_page)
    