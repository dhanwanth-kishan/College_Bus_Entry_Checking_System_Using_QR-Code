from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StudentData(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    Name=models.CharField(max_length=30,null=True,blank=True)
    Stud_id=models.IntegerField(null=True,blank=True)
    Department=models.CharField(max_length=30,null=True,blank=True)
    Phone_Number=models.IntegerField(null=True,blank=True)
    Bus_Number=models.IntegerField(null=True,blank=True)
    Bus_Route=models.CharField(max_length=30,null=True,blank=True)
    Stud_Profile_Pic=models.ImageField(upload_to="student_profile_pic",null=True,blank=True)
    Qr_Code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)


    
    def __str__(self):
      return self.Name
  


class StaffData(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    Name=models.CharField(max_length=30,null=True,blank=True)
    Staff_id=models.IntegerField(null=True,blank=True)
    Phone_Number=models.IntegerField(null=True,blank=True)
    Bus_Number=models.IntegerField(null=True,blank=True)
    Bus_Route=models.CharField(max_length=30,null=True,blank=True)
    Staff_Profile_Pic=models.ImageField(upload_to="staff_profile_pic",null=True,blank=True)
      
    def __str__(self):
      return self.Name
  

class BusData(models.Model):
    Bus_No=models.IntegerField(null=True,blank=True)
    Bus_Route=models.CharField(null=True,blank=True)
    Arrival=models.TimeField(null=True,blank=True)
    Departure=models.TimeField(null=True,blank=True)
    


class BusEntry(models.Model):
    student = models.ForeignKey(StudentData, on_delete=models.CASCADE)
    staff = models.ForeignKey(StaffData, on_delete=models.CASCADE, related_name='entries_done')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)


class GetINTouch(models.Model):
   Name=models.CharField(max_length=30)
   Number=models.IntegerField(null=True)
   Email=models.EmailField(max_length=30)
   Subject=models.CharField(max_length=30)
   Message=models.TextField(null=True)
  

