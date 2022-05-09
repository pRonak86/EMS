from datetime import datetime

from django.db import models

# Create your models here.

class Employee(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    contact = models.IntegerField()
    gender = models.CharField(max_length=20)
    dob=models.DateField()
    address=models.CharField(max_length=30)
    state=models.CharField(max_length=20)
    bloodGroup=models.CharField(max_length=20)
    managerName=models.CharField(max_length=30,null=True)
    managerId = models.CharField(max_length=20, null=True)
    joinDate=models.DateField(null=True)
    salary=models.IntegerField(null=True, default=30000)
    leave=models.IntegerField(null=True, default=14)
    qualification=models.CharField(max_length=30)
    activation_Date = models.DateTimeField(null=True)
    deactivation_Date = models.DateTimeField(null=True)
    account = models.CharField(max_length=20, default="Deactive")
    emailId=models.EmailField()
    password=models.CharField(max_length=20)
    resume = models.FileField(upload_to='documents', null=True)
    about = models.CharField(max_length=40, null=True)
    image =models.ImageField(upload_to='images/', null=True)
    empCode = models.CharField(primary_key=True, editable=False, max_length=10, unique=True,default="None")

    def save(self, **kwargs):
        no = Employee.objects.count()  # Count method is used to count object form the Employee table
        if no == None:
            no = 1
        else:
            no = no + 1
        self.empCode = "{}{:03}".format('EMP', no)
        super().save(*kwargs)


class Manager(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    contact = models.IntegerField()
    gender = models.CharField(max_length=20)
    dob=models.DateField()
    address=models.CharField(max_length=30)
    state=models.CharField(max_length=20)
    bloodGroup=models.CharField(max_length=20)
    joinDate=models.DateField(null=True)
    salary = models.IntegerField(null=True, default=30000)
    leave = models.IntegerField(null=True, default=14)
    qualification=models.CharField(max_length=30)
    activation_Date = models.DateTimeField(null=True)
    deactivation_Date = models.DateTimeField(null=True)
    account = models.CharField(max_length=20, default="Deactive")
    emailId=models.EmailField()
    password=models.CharField(max_length=20)
    about = models.CharField(max_length=40, null=True)
    managerCode = models.CharField(primary_key=True, editable=False, max_length=10, unique=True, default="None")
    image = models.ImageField(upload_to='images/', null=True)
    resume = models.FileField(upload_to='documents',null=True)

    def save(self, **kwargs):
        no = Manager.objects.count()  # Count method is used to count object form the Employee table
        if no == None:
            no = 1
        else:
            no = no + 1
        self.managerCode = "{}{:03}".format('MANAGER', no)
        super().save(*kwargs)


class client(models.Model):
    clientId=models.IntegerField(primary_key=True)
    managerName = models.CharField(max_length=30, null=True)
    managerId = models.CharField(max_length=20, null=True)
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    phone=models.IntegerField()
    gender=models.CharField(max_length=20)
    companyName=models.CharField(max_length=40)
    companyAddress=models.CharField(max_length=40)
    companyState=models.CharField(max_length=20)
    emailId = models.EmailField()
    password=models.CharField(max_length=20)
    companyDescription=models.CharField(max_length=40)
    registration_Date = models.DateTimeField(default=datetime.now, blank=True)
    activation_Date = models.DateTimeField(null=True)
    deactivation_Date = models.DateTimeField(null=True)
    image = models.ImageField(upload_to='images/', null=True)
    account = models.CharField(max_length=20, default="Deactive")

class Holidays(models.Model):
    hoildayId = models.IntegerField(primary_key=True)
    holidayName = models.CharField(max_length=20)
    hoildayDescription = models.CharField(max_length=30)
    hoildayDate = models.DateField()
    hoildayDay = models.CharField(max_length=20)

class clientProject(models.Model):
    projectId = models.IntegerField(primary_key=True)
    clientId = models.IntegerField()
    managerId = models.CharField(max_length=20,null=True)
    projectName = models.CharField(max_length=20, null=True)
    projectDescription = models.CharField(max_length=60)
    totalDays = models.IntegerField()
    otherDays = models.IntegerField(null=True)
    createdDate = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(max_length=20, null=True)
    deadlineDate = models.DateField(null=True)
    fileUpload1 = models.FileField(upload_to='documents', null=True)
    fileUpload2 = models.FileField(upload_to='documents',null=True)
    cost = models.IntegerField(null=True)


class Leave(models.Model):
    leaveId = models.IntegerField(primary_key=True)
    employeeId = models.CharField(max_length=20)
    employeeName = models.CharField(max_length=20, null=True)
    managerId = models.CharField(max_length=20, null=True)
    startDate = models.DateField()
    endDate = models.DateField()
    totalDays = models.IntegerField(default=0)
    employeeReason = models.CharField(max_length=40)
    managerReason = models.CharField(max_length=40)
    appliedDate = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(max_length=10)
    leaveType = models.CharField(max_length=20, null=True)

class employeeDailyWork(models.Model):
    id = models.IntegerField(primary_key=True)
    employeeId = models.CharField(max_length=20)
    employeeName = models.CharField(max_length=20, null=True)
    managerId = models.CharField(max_length=20)
    clientId = models.IntegerField(null=True)
    workDescription = models.CharField(max_length=40,null=True)
    loginTime = models.DateTimeField()
    loginHour = models.TimeField(null=True)
    logoutTime = models.DateTimeField(null=True)
    logoutHour = models.TimeField(null=True)
    date = models.DateField(null=True)
    projectId = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    image = models.ImageField(upload_to='images/', null=True)

class perDaySalary(models.Model):
    empCode=models.CharField(max_length=20)
    date=models.DateField()
    totalTime = models.IntegerField()
    daySalary = models.IntegerField()

class tasks(models.Model):
    id = models.IntegerField(primary_key=True)
    employeeId = models.CharField(max_length=20)
    employeeName = models.CharField(max_length=20,null=True)
    managerId = models.CharField(max_length=20)
    clientId = models.IntegerField(null=True)
    projectName = models.CharField(max_length=20,null=True)
    date = models.DateField()
    workDescription = models.CharField(max_length=40, null=True)
    fileUpload = models.FileField(upload_to='documents',null=True)

class Attendance(models.Model):
    id = models.IntegerField(primary_key=True)
    employeeId = models.CharField(max_length=20)
    employeeName = models.CharField(max_length=20, null=True)
    date = models.DateField()
    loginTime = models.DateTimeField()
    logoutTime = models.DateTimeField()
    status = models.CharField(max_length=20, default='Absent')
    absentStatus = models.CharField(max_length=20, null=True)

class monthSalary(models.Model):
    id = models.IntegerField(primary_key=True)
    empCode=models.CharField(max_length=20)
    dateCreated=models.DateTimeField(null=True)
    date = models.DateField(null=True)
    month = models.CharField(max_length=20,null=True)
    year = models.IntegerField(null=True)
    totalTime = models.IntegerField()
    finalSalary = models.IntegerField()
    status = models.CharField(max_length=20,null=True)

class admin(models.Model):
    id = models.IntegerField(primary_key=True)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    contact = models.IntegerField()
    gender = models.CharField(max_length=10)
    emailId = models.EmailField()
    password = models.CharField(max_length=20)

class notice(models.Model):
    id = models.IntegerField(primary_key=True)
    noticeDetails = models.CharField(max_length=100)
    noticeDate = models.DateField(default=datetime.now)

class Notice1(models.Model):
    id = models.IntegerField(primary_key=True)
    noticeDetails = models.CharField(max_length=100)
    noticeDate = models.DateField(default=datetime.now)


