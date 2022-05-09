from datetime import datetime
from django.core.mail import EmailMessage
from itertools import count

from django.db.models import Q, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse

from EMS.models import Employee, Manager, client, Holidays, clientProject, Leave, employeeDailyWork, tasks, \
    perDaySalary, Attendance, monthSalary, admin, notice, Notice1
from EmployeeManagementSystem.settings import EMAIL_HOST_USER


#-------------------------others ------------------------------


def managerRegistration(request):
    return render(request, "managerRegistration.html")

def saveManager(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    phone = request.POST['phone']
    gender = request.POST['gender']
    bloodGroup = request.POST['bloodGroup']
    dob=request.POST['dob']
    address = request.POST['address']
    state=request.POST['state']
    qualification=request.POST['qualification']
    emailId = request.POST['email']
    password = request.POST['password']
    image = request.FILES['image']
    resume = request.FILES['resume']

    e = Manager(fname=fname, lname=lname, contact=phone, gender=gender,bloodGroup=bloodGroup,
                 dob=dob, address=address, state=state,  qualification=qualification,
                 emailId=emailId, password=password, image=image, resume=resume)
    e.save()
    if e:
        msg = "Your Application has been Submited. We will Back to you Soon"
        return render(request, "managerRegistration.html", {'msg': msg})
    else:
        return HttpResponse("error")

def managerLogin(request):
    return render(request, "managerLogin.html")

def loginManager(request):
    emailId = request.POST['email']
    password = request.POST['password']
    c = Manager.objects.filter(emailId=emailId, password=password,account='Active')
    if c:
        request.session['mngid'] = c[0].managerCode
        request.session['managerFname'] = c[0].fname
        request.session['managerLname'] = c[0].lname
       # request.session['img'] = c[0].image
        date = datetime.now().date()
        '''
        c = Attendance.objects.filter(employeeId=request.session['mngid'], date=date)
        if not c:
            attendance = Attendance(employeeId=request.session['mngid'], loginTime=time, logoutTime=time, date=date,
                                    status='Present')
            attendance.save()
        else:
            print('OK')
        '''
        return HttpResponseRedirect(reverse("managerDashboard"))
    else:
        msg = 'You Are Not Valid User'
        return render(request, "managerLogin.html", {'msg': msg})

def clientRegistration(request):
    return render(request, "clientRegistration.html")

def saveClient(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    contact = request.POST['contact']
    gender = request.POST['gender']
    companyName = request.POST['companyName']
    companyAddress = request.POST['companyAddress']
    companyState = request.POST['companyState']
    companyDescription = request.POST['companyDescription']
    email = request.POST['email']
    password = request.POST['password']
    image = request.FILES['image']
    c = client(fname=fname,lname=lname,phone=contact,gender=gender,companyName=companyName,
               companyAddress=companyAddress,companyState=companyState,companyDescription=companyDescription,
               emailId=email,password=password, image=image)
    c.save()
    if c:
        msg = "Your Application has been Submited. We will Back to you Soon"
        return render(request, "clientRegistration.html", {'msg': msg})
    else:
        return HttpResponse("error")

def clientLogin(request):
    return render(request, "clientLogin.html")

def loginClient(request):
    emailId = request.POST['email']
    password = request.POST['password']
    c = client.objects.filter(emailId=emailId, password=password)
    if c:
        request.session['cid'] = c[0].clientId
        request.session['fname'] = c[0].fname
        request.session['lname'] = c[0].lname
        request.session['manager'] = c[0].managerId
        return HttpResponseRedirect(reverse("clientDashboard"))
    else:
        msg = 'You Are Not The Valid User'
        return render(request, "clientLogin.html", {'msg': msg})

def employeeRegistration(request):
    return render(request, "employeeRegistration.html")

def saveEmployee(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    phone = request.POST['phone']
    gender = request.POST['gender']
    bloodGroup = request.POST['bloodGroup']
    dob=request.POST['dob']
    address = request.POST['address']
    state=request.POST['state']
    qualification=request.POST['qualification']
    emailId = request.POST['email']
    password = request.POST['password']
    image = request.FILES['image']
    resume = request.FILES['resume']

    e = Employee(fname=fname, lname=lname, contact=phone, gender=gender,bloodGroup=bloodGroup,
                 dob=dob, address=address, state=state,  qualification=qualification,
                 emailId=emailId, password=password, image=image, resume=resume)
    e.save()
    if e:
        msg = "Your Application has been Submited. We will Back to you Soon"
        return render(request, "employeeRegistration.html", {'msg': msg})
    else:
        return HttpResponse("error")

def employeeLogin(request):
    return render(request, "employeeLogin.html")

def loginEmployee(request):
    emailId = request.POST['email']
    password = request.POST['password']
    c = Employee.objects.filter(emailId=emailId, password=password,account='Active')
    if c:
        time = datetime.now()
        date = datetime.now().date()
        request.session['empid'] = c[0].empCode
        request.session['fname'] = c[0].fname
        request.session['lname'] = c[0].lname
        request.session['managerId'] = c[0].managerId
        request.session['leave'] = c[0].leave
        employeeName = request.session['fname'] + request.session['lname']
        res = employeeDailyWork(employeeId=c[0].empCode, managerId=c[0].managerId,loginTime=time,date=date)
        res.save()
        eid = employeeDailyWork.objects.latest('id')
        feid = eid.id
        request.session['workId'] = feid
        print(feid)

        c = Attendance.objects.filter(employeeId=request.session['empid'], date=date)
        if not c:
            attendance = Attendance(employeeId=request.session['empid'], loginTime=time, logoutTime=time, date=date,
                                    status='Present', employeeName=employeeName)
            attendance.save()
        else:
            print('OK')
        return HttpResponseRedirect(reverse("employeeDashboard"))
    else:
        msg = 'You Are Not Valid User'
        return render(request, "employeeLogin.html", {'msg': msg})

def aboutUs(request):
    return render(request, "aboutUs.html")

def jobList(request):
    return render(request, 'jobList.html')

def jobDetails(request):
    return render(request, 'jobDetails.html')

def jobDetailsManager(request):
    return render(request, 'jobDetailsManager.html')

def adminlogin(request):
    return render(request, 'adminLogin.html')

def loginAdmin(request):
    emailId = request.POST['email']
    password = request.POST['password']
    c = admin.objects.filter(emailId=emailId, password=password)
    if c:
        return HttpResponseRedirect(reverse("adminDashboard"))
       # return render(request, 'adminDashboard/index.html')
    else:
        msg = 'You Are Not The Valid User'
        return render(request, "adminLogin.html", {'msg': msg})

#------------ Admin -------------
def index(request):
    return render(request, "index.html")

def newAdmin(request):
    return render(request, "adminDashboard/newAdmin.html")

def saveAdmin(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    phone = request.POST['contact']
    gender = request.POST['gender']
    emailId = request.POST['email']
    password = request.POST['password']
    r = admin(fname=fname, lname=lname, contact=phone, gender=gender, emailId=emailId, password=password)
    r.save()
    if r:
        return HttpResponseRedirect(reverse("adminDashboard"))
    else:
        HttpResponseRedirect("Registration Failed")

def adminDetails(request):
    r = admin.objects.all()
    return render(request, "adminDashboard/adminDetails.html", {'r': r})


def adminIndexPage(request):
    employee = Employee.objects.filter(account='Active').count()
    manager = Manager.objects.filter(account='Active').count()
    clientTotal = client.objects.filter(account='Active').count()
    projectTotal = clientProject.objects.all().count()
    p = clientProject.objects.filter(status='Working')
    l = list(p)
    for i in l:
        #m = get_object_or_404(Manager, managerCode=i.managerId)
        m = Manager.objects.filter(managerCode=i.managerId)
        print(m)
    param = {'m': m, 'p': p, 'employee': employee, 'manager': manager, 'clientTotal': clientTotal,'projectTotal': projectTotal}
    return render(request, "adminDashboard/index.html", param)

def base(request):
    return render(request, "adminDashboard/base.html")

def projectProgressAdmin(request,pk):
    pj = get_object_or_404(clientProject, pk=pk)
    pid =pj.projectId
    m = pj.managerId
    mng = Manager.objects.filter(managerCode=m)
    emp = Employee.objects.filter(managerId=m)

    p = employeeDailyWork.objects.filter(projectId=pid).order_by('-id')

    param = {'emp': emp, 'mng': mng, 'pj': pj, 'p': p}
    return render(request, "adminDashboard/projectProgress.html", param)

def employeeRequest(request):
    e1 = Employee.objects.filter(account='Deactive')
    return render(request, "adminDashboard/employeeRequest.html", {'e1': e1})

def managerRequest(request):
    e1 = Manager.objects.filter(account='Deactive')
    return render(request, "adminDashboard/managerRequest.html", {'e1': e1})

def clientRequest(request):
    e1 = client.objects.filter(account='Deactive')
    return render(request, "adminDashboard/clientRequest.html", {'e1': e1})

def projectRequest(request):
    p = clientProject.objects.filter(status='Working')
    m = p[0].managerId
    mng = Manager.objects.filter(managerCode=m)
    emp = Employee.objects.filter(managerId=m)
    c = p[0].clientId
    clt = client.objects.filter(clientId=c)
    return render(request, "adminDashboard/projectRequest.html", {'p': p, 'clt': clt, 'mng': mng, 'emp': emp})

def projectView(request,pk):
    pj = get_object_or_404(clientProject, pk=pk)
    m = pj.managerId
    mng = Manager.objects.filter(managerCode=m)
    emp = Employee.objects.filter(managerId=m)
    return render(request, "adminDashboard/projectView.html", {'emp':emp, 'pj': pj, 'mng': mng})

def allProject(request):
    p1 = clientProject.objects.all()
    m = p1[0].managerId
    mng = Manager.objects.filter(managerCode=m)
    emp = Employee.objects.filter(managerId=m)
    return render(request, "adminDashboard/allProject.html", {'p1': p1, 'mng': mng, 'emp': emp})

def allEmployee(request):
    e1 = Employee.objects.filter(account='Active')
    return render(request, "adminDashboard/allEmployee.html", {'e1': e1})

def allManager(request):
    e1 = Manager.objects.filter(account='Active')
    return render(request, "adminDashboard/allManager.html", {'e1': e1})

def allClient(request):
    e1 = client.objects.filter(account='Active')
    return render(request, "adminDashboard/allClient.html", {'e1': e1})

def editEmployee(request,pk):
    e = get_object_or_404(Employee, empCode=pk)
    e1 = e.managerId
    m = Manager.objects.filter(managerCode=e1)
    fname = m[0].fname
    lname = m[0].lname
    return render(request, "adminDashboard/editEmployee.html", {'e': e, 'fname': fname, 'lname': lname})

def editManager(request,pk):
    e = get_object_or_404(Manager, managerCode=pk)
    return render(request, "adminDashboard/editManager.html",  {'e': e})

def editClient(request,pk):
    e = get_object_or_404(client, clientId=pk)
    e1 = e.managerId
    m = Manager.objects.filter(managerCode=e1)
    fname = m[0].fname
    lname = m[0].lname
    return render(request, "adminDashboard/editClient.html",  {'e': e, 'fname': fname, 'lname': lname})

def updateEmployee(request):
    id = request.POST['id']
    fname = request.POST['fname']
    lname = request.POST['lname']
    phone = request.POST['phone']
    bloodGroup = request.POST['bloodGroup']
    address = request.POST['address']
    state = request.POST['state']
    qualification = request.POST['qualification']
    emailId = request.POST['email']
    password = request.POST['password']
    leave = request.POST['leave']
    account = request.POST['account']
    e = Employee.objects.filter(empCode=id).update(fname=fname, lname=lname, contact=phone,
                  bloodGroup=bloodGroup, address=address, state=state, qualification=qualification,
                  emailId=emailId, password=password, account=account, leave=leave)
    if e:
        return HttpResponseRedirect(reverse('allEmployee'))
    else:
        return HttpResponse("Record Not Updated")

def updateManager(request):
    id = request.POST['id']
    fname = request.POST['fname']
    lname = request.POST['lname']
    phone = request.POST['phone']
    bloodGroup = request.POST['bloodGroup']
    address = request.POST['address']
    state = request.POST['state']
    qualification = request.POST['qualification']
    emailId = request.POST['email']
    password = request.POST['password']
    account = request.POST['account']
    Manager.objects.filter(managerCode=id).update(fname=fname,lname=lname,contact=phone,
                            bloodGroup=bloodGroup,address=address,state=state,qualification=qualification,
                            emailId=emailId,password=password,account=account)
    return HttpResponseRedirect(reverse('allManager'))

def updateClient(request):
    id = request.POST['id']
    fname = request.POST['fname']
    lname = request.POST['lname']
    contact = request.POST['phone']
    companyName = request.POST['companyName']
    companyAddress = request.POST['companyAddress']
    companyState = request.POST['companyState']
    companyDescription = request.POST['companyDescription']
    managerName = request.POST['managerName']
    email = request.POST['email']
    password = request.POST['password']

    client.objects.filter(clientId=id).update(fname=fname, lname=lname, phone=contact, companyName=companyName,
               companyAddress=companyAddress, companyState=companyState, companyDescription=companyDescription,managerName=managerName,
               emailId=email, password=password)
    return HttpResponseRedirect(reverse('allClient'))


def deleteEmployee(request,pk):
    emp = get_object_or_404(Employee, empCode=pk)
    emp.delete()
    return HttpResponseRedirect(reverse('allEmployee'))

def deleteManager(request,pk):
    mng = get_object_or_404(Manager, managerCode=pk)
    mng.delete()
    return HttpResponseRedirect(reverse('allManager'))

def employeeProfile(request,pk):
    emp = get_object_or_404(Employee, pk=pk)
    n = emp.managerId
    mng = Manager.objects.get(managerCode=n)
    return render(request, "adminDashboard/employeeProfile.html", {'emp': emp, 'mng': mng})

def managerProfile(request,pk):
    mng = get_object_or_404(Manager, pk=pk)
    return render(request, "adminDashboard/managerProfile.html", {'mng': mng})

def clientProfile(request, pk):
    ct = get_object_or_404(client, pk=pk)
    cltProject = clientProject.objects.filter(clientId=pk)
    return render(request, "adminDashboard/clientProfile.html", {'ct': ct, 'cltProject': cltProject})

def employeeRequestView(request,pk):
    emp = get_object_or_404(Employee, pk=pk)
    mng = Manager.objects.filter(account='Active')
    return render(request, "adminDashboard/employeeRequestView.html", {'emp': emp, 'mng': mng})

def clientRequestView(request,pk):
    ct = get_object_or_404(client, pk=pk)
    mng = Manager.objects.filter(account='Active')
    return render(request, "adminDashboard/clientRequestView.html", {'ct': ct, 'mng': mng})

def managerRequestView(request,pk):
    mng = get_object_or_404(Manager, pk=pk)
    request.session['id'] = mng.managerCode
    return render(request, "adminDashboard/managerRequestView.html", {'mng': mng})

def assignManager(request):
    id = request.POST['id']
    manager = request.POST['manager']
    joindate = request.POST['joinDate']
    activationDate = datetime.now()
    print(activationDate)
    msg = 'You have been Seleted for the Web Developer.'\
          'We are so happy to have you on our team, We are pleased to extend the following offer of employment to you on behalf of FOCUSE INFOTECH.' \
           \
          ''
    body = 'CONGRATULATIONS... !!!'
    email = 'neetu1998singh@gmail.com'
    e1 = EmailMessage(body, msg, EMAIL_HOST_USER, [email])
    e1.content_subtype = "html"
    e1.send()
    Employee.objects.filter(empCode=id).update(managerId=manager,joinDate=joindate,account='Active',
                                               activation_Date=activationDate)
    return HttpResponseRedirect(reverse("employeeRequest"))

def managerRequestEdit(request):
    id = request.POST['id']
    joindate = request.POST['joinDate']
    activationDate = datetime.now()
    Manager.objects.filter(managerCode=id).update(joinDate=joindate, account='Active',
                                               activation_Date=activationDate)
    return HttpResponseRedirect(reverse("managerRequest"))

def assignManagerClient(request):
    id = request.POST['id']
    manager = request.POST['manager']
    activationDate = datetime.now()
    client.objects.filter(clientId=id).update(managerId=manager,account='Active',activation_Date=activationDate)
    return HttpResponseRedirect(reverse("clientRequest"))

def hoildays(request):
    e1 = Holidays.objects.all()
    return render(request, "adminDashboard/hoildays.html", {'e1': e1})

def saveHoilday(request):
    holidayName = request.POST['holidayName']
    hoildayDate = request.POST['hoildayDate']
    hoildayDay = request.POST['hoildayDay']
    hoildayDescription = request.POST['hoildayDescription']

    h = Holidays(holidayName=holidayName, hoildayDate=hoildayDate, hoildayDay= hoildayDay, hoildayDescription=hoildayDescription)
    h.save()
    return HttpResponseRedirect(reverse("hoildays"))

def employeeStatus(request):
    #t = tasks.objects.all()
    t = tasks.objects.filter(date=datetime.now().date())
    if t:
        c = t[0].clientId
        clt = client.objects.filter(clientId=c)
        return render(request, "adminDashboard/employeeStatus.html", {'t': t, 'clt': clt})
    else:
        msg = 'No Task Allocated'
        return render(request, "adminDashboard/employeeStatus.html", {'t': t, 'msg': msg})


def showStatus(request):
    s = get_object_or_404(employeeDailyWork)
    return render(request, "adminDashboard/showStatus.html", {'s': s})

def filterEmployee(request):
    emp = Employee.objects.filter(account='Active')
    return render(request, "adminDashboard/filterEmployee.html", {'emp': emp})

def savefilterEmployee(request):
    employeeId = request.POST['employeeId']
    date = request.POST['date']
    res = employeeDailyWork.objects.filter(employeeId=employeeId, date=date)
    p =perDaySalary.objects.filter(empCode=employeeId, date=date)
    return render(request, "adminDashboard/filterEmployee.html", {'res': res, 'p': p})

def attendance(request):
    date = datetime.now().date()
    s = Attendance.objects.filter(date=date)
    param = {'s': s}
    return render(request, 'adminDashboard/attendance.html', param)

def attendanceFilter(request):
    return render(request, 'adminDashboard/attendanceFilter.html')

'''
# a = e[0].empCode
    e1 = []
    l = list(s)
    print("Test ",l)
    if l:
        for i in l:
            id=i.id
            print(id)
            e1 = get_object_or_404(Attendance, id=id)
            print(e1.loginTime)
           # print("Inside for ",ss)
           # e1.append(ss)
            print("outside for ",e1)
   
'''

def salary(request):
    e = Employee.objects.filter(account='Active')
    return render(request, "adminDashboard/salary.html", {'e': e})

def salaryView(request):
    employeeId = request.session['empid']
    c = monthSalary.objects.filter(empCode=employeeId)
    return render(request, "adminDashboard/salaryView.html", {'c': c})

def genrateSalary(request,pk):
    employeeId = get_object_or_404(Employee,empCode=pk)
    id = employeeId.empCode
    print(employeeId)
    date = datetime.now().date()
    mon = date.strftime('%B')
    year = date.year
    print(mon)
    print(year)
    items = perDaySalary.objects.filter(empCode=id)
    totalSalary1 = sum(items.values_list('daySalary', flat=True))
    totalSalary = totalSalary1 + 400 + 400 + 400
    totalTime = sum(items.values_list('totalTime', flat=True))
    print(totalSalary)
    print(totalTime)
    s = monthSalary.objects.filter(empCode=id, month=mon, year=year)
    if s:
        pass
    else:
        SalaryCal = monthSalary(empCode=id, dateCreated=datetime.now(), month=mon, year=year,
                                totalTime=totalTime, finalSalary=totalSalary,status='Paid')
        SalaryCal.save()
    c = monthSalary.objects.get(empCode=id)
    return render(request, "adminDashboard/salaryView.html", {'e': employeeId, 'c': c, 'totalTime': totalTime, 'totalSalary': totalSalary})

def adminLeave(request):
    l = Leave.objects.filter(status='Pending')
    n = l[0].employeeId
    name = Employee.objects.filter(empCode=n)
    return render(request, "adminDashboard/leave.html", {'l': l, 'name':name})

def notice(request):
    return render(request, "adminDashboard/notice.html")

def saveNotice(request):
    n = request.POST['notice']
    activationDate = datetime.now().date()
    r = Notice1(noticeDetails=n, noticeDate=activationDate)
    r.save()
    if r:
        return render(request, "adminDashboard/notice.html")

def reportEmployee(request):
    s = Employee.objects.filter(account="Active")
    return render(request, "adminDashboard/reportEmployee.html", {'s': s})

def reportManager(request):
    s = Manager.objects.filter(account="Active")
    return render(request, "adminDashboard/reportManager.html", {'s': s})

def reportClient(request):
    s = client.objects.filter(account="Active")
    return render(request, "adminDashboard/reportClient.html", {'s': s})

def reportEmployeeFilter(request):
    return render(request, "adminDashboard/reportEmployeeFilter.html")

def searchReportEmployeeFilter(request):
    date1 = request.POST['date1']
    date2 = request.POST['date2']
    status = request.POST['status']
    r = Employee.objects.filter(joinDate__range=[date1,date2],account=status)
    if r:
        return render(request, "adminDashboard/reportEmployeeFilter.html", {'r': r})
    else:
        msg = 'No Record Found'
        return render(request, "adminDashboard/reportEmployeeFilter.html", {'msg': msg})

def reportProject(request):
    return render(request, "adminDashboard/reportProject.html")

def searchReportProjectFilter(request):
    date1 = request.POST['date1']
    date2 = request.POST['date2']
    status = request.POST['status']
    r = clientProject.objects.filter(createdDate__range=[date1, date2], status=status)
    if r:
        return render(request, "adminDashboard/reportProject.html", {'r': r})
    else:
        msg = 'No Record Found'
        return render(request, "adminDashboard/reportProject.html", {'msg': msg})



#-------------------------Client Dashboard ----------------------------
def Cbase(request):
    if request.session.has_key('cid'):
        return render(request, "clientDashboard/base.html", )
    else:
        return render(request, "clientLogin.html")

def clientIndexPage(request):
    if request.session.has_key('cid'):
        id = request.session['cid']
        fname = request.session['fname']
        lname = request.session['lname']
        cltImage = get_object_or_404(client, clientId=id)
        p = clientProject.objects.filter(clientId=id)
        tProject = clientProject.objects.filter(clientId=id).count()
        time = datetime.now().time()
        param = {'fname': fname, 'lname': lname, 'p': p, 'tProject': tProject, 'time': time, 'cltImage': cltImage}
        return render(request, "clientDashboard/index.html", param)
    else:
        return render(request, "clientLogin.html")

def addProject(request):
    if request.session.has_key('cid'):
        fname = request.session['fname']
        lname = request.session['lname']
        id = request.session['cid']
        cltImage = get_object_or_404(client, clientId=id)
        param = {'fname': fname, 'lname': lname, 'cltImage': cltImage}
        return render(request, "clientDashboard/addProject.html", param)
    else:
        return render(request, "clientLogin.html")

def saveProject(request):
    mng = request.session['manager']
    cltId = request.session['cid']
    totalDays = request.POST['totalDays']
    projectName = request.POST['projectName']
    projectDescription = request.POST['projectDescription']
    deadlineDate = request.POST['deadlineDate']
    cost = request.POST['cost']
    document = request.FILES['document']
    cltProject = clientProject(managerId=mng, clientId=cltId, projectName=projectName, projectDescription=projectDescription,
                               totalDays=totalDays, deadlineDate=deadlineDate, status='Working', cost=cost, fileUpload1=document)
    cltProject.save()
    if cltProject:
        return HttpResponseRedirect(reverse('projectClient'))

def profileClient(request):
    if request.session.has_key('cid'):
        fname = request.session['fname']
        lname = request.session['lname']
        cltId = request.session['cid']
        id = request.session['cid']
        cltImage = get_object_or_404(client, clientId=id)

        c = client.objects.get(clientId=cltId)
        param = {'fname': fname, 'lname': lname, 'c': c, 'cltImage':cltImage}
        return render(request, "clientDashboard/profile.html", param)
    else:
        return render(request, "clientLogin.html")

def saveProfileClient(request):
    cltId = request.session['cid']
    fname = request.POST['fname']
    lname = request.POST['lname']
    contact = request.POST['contact']
    companyName = request.POST['companyName']
    companyAddress = request.POST['companyAddress']
    companyState = request.POST['companyState']
    companyDescription = request.POST['companyDescription']
    email = request.POST['email']
    client.objects.filter(clientId=cltId).update(fname=fname, lname=lname, phone=contact,companyName=companyName,
               companyAddress=companyAddress, companyState=companyState, companyDescription=companyDescription,
               emailId=email)
    return render(request, "clientDashboard/profile.html")

def projectClient(request):
    if request.session.has_key('cid'):
        fname = request.session['fname']
        lname = request.session['lname']
        cltId = request.session['cid']
        id = request.session['cid']
        cltImage = get_object_or_404(client, clientId=id)
        c = clientProject.objects.filter(clientId=cltId).order_by('-projectId')
        if c:
            m = c[0].managerId
            managerName = Manager.objects.get(managerCode=m)
            param = {'fname': fname, 'lname': lname, 'c': c, 'managerName': managerName, 'cltImage':cltImage}
            return render(request, "clientDashboard/projects.html", param)
        else:
            msg = 'No Project Right Now'
            param = {'fname': fname, 'lname': lname, 'msg': msg, 'cltImage':cltImage}
            return render(request, "clientDashboard/projects.html", param)
    else:
        return render(request, "clientLogin.html")

def projectProgress(request,pk):
    if request.session.has_key('cid'):
        fname = request.session['fname']
        lname = request.session['lname']
        id = request.session['cid']
        cltImage = get_object_or_404(client, clientId=id)
        p = employeeDailyWork.objects.filter(projectId=pk).order_by('-id')
        if p:
            eid = p[0].employeeId
            e = Employee.objects.filter(empCode=eid)
            pName = clientProject.objects.get(projectId=p[0].projectId)
            param = {'fname': fname, 'lname': lname, 'p': p, 'e': e, 'cltImage':cltImage, 'pName': pName}
            return render(request, "clientDashboard/projectProgress.html", param)
        else:
            msg = 'No Project Progress'
            param = {'fname': fname, 'lname': lname, 'msg': msg, 'p': p, 'cltImage': cltImage }
            return render(request, "clientDashboard/projectProgress.html", param)
    else:
        return render(request, "clientLogin.html")

def clientChangePassword(request):

    if request.session.has_key('cid'):
        fname = request.session['fname']
        lname = request.session['lname']
        id = request.session['cid']
        '''
        oldPassword = request.POST['oldPassword']
        newPassword = request.POST['newPassword']
        confirmPassword = request.POST['confirmPassword']
        cltImage = get_object_or_404(client, clientId=id)

        oldpwd = client.objects.filter(clientId=id)
        print(oldpwd[0].password)

        if oldPassword == oldpwd[0].password:
            if newPassword == confirmPassword:
                client.objects.filter(clientId=id).update(password=newPassword)
                msg = "Your Password Has Been Changed"
                return render(request, "clientDashboard/changePassword.html",
                              {'msg': msg, 'fname': fname, 'lname': lname, 'cltImage': cltImage})
            else:
                msg = "New Password And Confirm Password must be same"
                return render(request, "clientDashboard/changePassword.html",
                              {'msg': msg, 'fname': fname, 'lname': lname, 'cltImage': cltImage})
        else:
            msg = "Old Password is Incorrect"
            return render(request, "clientDashboard/changePassword.html",
                          {'msg': msg, 'fname': fname, 'lname': lname, 'cltImage': cltImage})

'''
        return render(request, "clientDashboard/changePassword.html")
    else:
        return render(request, "clientDashboard/changePassword.html")
#----------------------------Employee Dashboard -------------------------------

def Ebase(request):
    if request.session.has_key('empid'):
        fname = request.session['fname']
        lname = request.session['lname']
        return render(request, "employeeDashboard/index.html", {'fname': fname, 'lname': lname})
    else:
        return render(request, "employeeLogin.html")


def employeeIndexPage(request):
    if request.session.has_key('empid'):
        fname =  request.session['fname']
        lname =  request.session['lname']
        eid = request.session['empid']
        m = request.session['managerId']
        img = Employee.objects.get(empCode=eid)
        id = request.session['empid']
        empImage = get_object_or_404(Employee, empCode=id)
        date = datetime.now().date()

        items = employeeDailyWork.objects.filter(employeeId=eid,date=date)
        tHour = Sum(items.values_list('duration', flat=True))
        print(tHour)
        lTime = Attendance.objects.get(employeeId=eid, date=date)
        p = clientProject.objects.filter(managerId=m, status='Working')
        n = Notice1.objects.filter()[:1].get()
        if p:
            pName = p[0].projectName
            print(pName)
            param = {'lTime': lTime, 'fname': fname, 'lname': lname, 'date': date, 'tHour': tHour,
                     'pName': pName, 'img': img, 'empImage':empImage, 'n': n}
            return render(request, "employeeDashboard/index.html", param)
        else:
            param = {'lTime': lTime, 'fname': fname, 'lname': lname, 'date': date, 'tHour': tHour,
                     'img': img, 'empImage': empImage}
            return render(request, "employeeDashboard/index.html", param)
    else:
        return render(request, "employeeLogin.html")

def employeeLeave(request):
    if request.session.has_key('empid'):
        fname = request.session['fname']
        lname = request.session['lname']
        managerId = request.session['managerId']
        id = request.session['empid']
        empImage = get_object_or_404(Employee, empCode=id)
        return render(request, "employeeDashboard/leave.html", {'fname': fname, 'lname': lname,
                'managerId': managerId, 'empImage': empImage})
    else:
        return render(request, "employeeLogin.html")

def saveLeave(request):
    fname = request.session['fname']
    lname = request.session['lname']
    eid = request.session['empid']
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']
    reason = request.POST['reason']
    totalDays = request.POST['totalDays']
    managerId = request.POST['manager_id']
    leaveType = request.POST['leaveType']
    ename = fname+ lname
    l = request.session['leave']
    print(ename)
    l = Leave(employeeId=eid, employeeName=ename, startDate=startDate, endDate=endDate,totalDays=totalDays, employeeReason=reason,
              status='Pending', managerId=managerId, leaveType=leaveType)
    l.save()
    if l:
        return HttpResponseRedirect(reverse("employeeLeave"))
    else:
        return HttpResponse("error")

def leaveStatus(request):
    if request.session.has_key('empid'):
        fname = request.session['fname']
        lname = request.session['lname']
        id = request.session['empid']
        empImage = get_object_or_404(Employee, empCode=id)
        param = {'fname': fname, 'lname': lname, 'empImage':empImage}
        return render(request, "employeeDashboard/leaveStatus.html", param)
    else:
        return render(request, "employeeLogin.html")

def searchLeaveStatus(request):
    leave = Leave.objects.all()
    empid = request.session['empid']
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']
    status = request.POST['status']
    id = request.session['empid']
    empImage = get_object_or_404(Employee, empCode=id)
    res = Leave.objects.filter(startDate__gte=startDate, startDate__lte=endDate,status=status,employeeId=empid)
    # res = Leave.objects.filter(startDate__gte=startDate,endDate__lte=endDate)
    return render(request, "employeeDashboard/leaveStatus.html", {'res': res, 'empImage':empImage})

def workUpload(request):
    if request.session.has_key('empid'):
        fname = request.session['fname']
        lname = request.session['lname']
        managerId = request.session['managerId']
        id = request.session['empid']
        empImage = get_object_or_404(Employee, empCode=id)
        c = client.objects.filter(managerId=managerId)
        return render(request, "employeeDashboard/workUpload.html", {'c' :c, 'fname': fname,
                'lname': lname, 'managerId': managerId, 'empImage':empImage})
    else:
        return render(request, "employeeLogin.html")

def saveWorkDone(request):
    fname = request.session['fname']
    lname = request.session['lname']
    managerId = request.session['managerId']
    empid = request.session['workId']
    date = request.POST['date']
    clientId = request.POST['clientId']
    workDescription = request.POST['workDone']
    employeeName = fname + lname
    id = request.session['empid']
    empImage = get_object_or_404(Employee, empCode=id)
    image1 = empImage.image
    p = clientProject.objects.filter(managerId=managerId,status='Working')
    proj = p[0].projectId
    employeeDailyWork.objects.filter(id=empid).update(date=date,clientId=clientId,
          projectId=proj,workDescription=workDescription, employeeName=employeeName, image=image1)
    return HttpResponseRedirect(reverse("workUpload"))

def userProfile(request):
    if request.session.has_key('empid'):
        fname = request.session['fname']
        lname = request.session['lname']
        id = request.session['empid']
        empImage = get_object_or_404(Employee, empCode=id)
        e = Employee.objects.get(empCode=id)
        param = {'fname': fname, 'lname': lname, 'e':e, 'empImage': empImage}
        return render(request, "employeeDashboard/userProfile.html", param)
    else:
        return render(request, "employeeLogin.html")

def saveUserProfile(request):
    id = request.session['empid']
    fname = request.POST['fname']
    lname = request.POST['lname']
    phone = request.POST['phone']
    bloodGroup = request.POST['bloodGroup']
    address = request.POST['address']
    gender = request.POST['gender']
    state = request.POST['state']
    qualification = request.POST['qualification']
    emailId = request.POST['email']
    e = Employee.objects.filter(empCode=id).update(fname=fname, lname=lname, contact=phone,
           bloodGroup=bloodGroup,address=address,gender=gender, state=state,qualification=qualification,
                emailId=emailId)
    if e:
        return render(request, "employeeDashboard/userProfile.html")
    else:
        return HttpResponse("Record Not Updated")

def projects(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        managerId = request.session['mngid']
        id = request.session['empid']
        empImage = get_object_or_404(Employee, empCode=id)
        p = clientProject.objects.filter(managerId=managerId).order_by('-projectId')
        l = list(p)
        projectName=p[0].projectName
        projectDescription = p[0].projectDescription
        clt = p[0].clientId
        cltName = client.objects.filter(clientId=clt)
        cfname = cltName[0].fname
        clname = cltName[0].lname

        deadLine = p[0].totalDays
        param = {'l':l, 'fname': fname, 'lname': lname,'projectName':projectName, 'projectDescription': projectDescription,
                  'deadLine': deadLine, 'cfname':cfname, 'clname':clname, 'empImage': empImage}
        return render(request, "managerDashboard/projects.html", param)
    else:
        return render(request, "managerLogin.html")

def projectEmployee(request):
    if request.session.has_key('empid'):
        fname = request.session['fname']
        lname = request.session['lname']
        managerId = request.session['managerId']
        id = request.session['empid']
        empImage = get_object_or_404(Employee, empCode=id)
        p = clientProject.objects.filter(managerId=managerId).order_by('-projectId')
        l = list(p)
        projectName = p[0].projectName
        projectDescription = p[0].projectDescription
        clt = p[0].clientId
        cltName = client.objects.filter(clientId=clt)
        cfname = cltName[0].fname
        clname = cltName[0].lname
        deadLine = p[0].totalDays
        param = {'l': l, 'fname': fname, 'lname': lname, 'projectName': projectName, 'projectDescription': projectDescription,
                 'deadLine': deadLine, 'cfname': cfname, 'clname': clname, 'empImage': empImage}
        return render(request, "employeeDashboard/projects.html", param)
    else:
        return render(request, "employeeLogin.html")

def employeeProjectView(request,pk):
    if request.session.has_key('empid'):
        fname = request.session['fname']
        lname = request.session['lname']
        id = request.session['empid']
        empImage = get_object_or_404(Employee, empCode=id)
        c = get_object_or_404(clientProject, pk=pk)
        clientName = c.clientId
        projectLeader = c.managerId
        m = Manager.objects.filter(managerCode=projectLeader)
        managerName = m[0].fname
        managerLname = m[0].lname
        cname = client.objects.get(clientId=clientName)
        emp = Employee.objects.filter(managerId=projectLeader)
        return render(request, 'employeeDashboard/projectView.html', {'cname':cname, 'fname': fname,'lname': lname, 'emp': emp,
            'c': c, 'managerName': managerName, 'managerLname': managerLname, 'empImage': empImage})

def changePassword(request):
    if request.session.has_key('empid'):
        fname = request.session['fname']
        lname = request.session['lname']
        managerId = request.session['managerId']
        id = request.session['empid']
        empImage = get_object_or_404(Employee, empCode=id)
        param = {'fname': fname, 'lname': lname, 'managerId': managerId, 'empImage': empImage}
        return render(request, "employeeDashboard/changePassword.html", param)
    else:
        return render(request, "employeeLogin.html")

def changePasswordEmployee(request):
    if request.session.has_key('empid'):
        fname = request.session['fname']
        lname = request.session['lname']
        employeeId = request.session['empid']
        oldPassword = request.POST['oldPassword']
        newPassword = request.POST['newPassword']
        confirmPassword = request.POST['comfirmPassword']
        id = request.session['empid']
        empImage = get_object_or_404(Employee, empCode=id)

        oldpwd = Employee.objects.filter(empCode=employeeId)
        oldpwd[0].password
        print(oldpwd[0].password)

        if oldPassword == oldpwd[0].password:
            if newPassword == confirmPassword:
                Employee.objects.filter(empCode=employeeId).update(password=newPassword)
                msg = "Your Password Has Been Changed"
                return render(request, "employeeDashboard/changePassword.html", {'msg': msg,'fname':fname, 'lname': lname, 'empImage': empImage})
            else:
                msg = "New Password And Confirm Password must be same"
                return render(request, "employeeDashboard/changePassword.html", {'msg': msg,'fname':fname, 'lname': lname, 'empImage': empImage})
        else:
            msg = "Old Password is Incorrect"
            return render(request, "employeeDashboard/changePassword.html", {'msg': msg,'fname':fname, 'lname': lname, 'empImage': empImage})

def tasksDetails(request):
    if request.session.has_key('empid'):
        id = request.session['empid']
        fname = request.session['fname']
        lname = request.session['lname']
        empImage = get_object_or_404(Employee, empCode=id)
        t = tasks.objects.filter(employeeId=id, date=datetime.now().date())
        if t:
            managerId = t[0].managerId
            clientId = t[0].clientId
            managerName = Manager.objects.filter(managerCode=managerId)
            clientName = client.objects.filter(clientId=clientId)
            param = {'fname': fname, 'lname': lname, 't': t, 'managerName': managerName, 'clientName': clientName, 'empImage':empImage}
            return render(request, "employeeDashboard/tasksDetails.html", param)
        else:
            msg = 'Today Task is Not Uploaded'
            return render(request, "employeeDashboard/tasksDetails.html", {'msg': msg, 'fname': fname, 'lname': lname, 'empImage': empImage})
    else:
        return render(request, "employeeLogin.html")

def paySlip(request):
    if request.session.has_key('empid'):
        id = request.session['empid']
        fname = request.session['fname']
        lname = request.session['lname']
        empImage = get_object_or_404(Employee, empCode=id)
        param = {'fname': fname, 'lname': lname, 'id': id, 'empImage': empImage}
        return render(request, "employeeDashboard/paySlip.html", param)

def searchPaySlip(request):
    if request.session.has_key('empid'):
        id = request.session['empid']
        empImage = get_object_or_404(Employee, empCode=id)
        fname = request.session['fname']
        lname = request.session['lname']
        e = request.POST['eid']
        month = request.POST['month']
        year = request.POST['year']
        s = monthSalary.objects.filter(empCode=e, month=month, year=year)
        param = {'fname': fname, 'lname': lname,'s': s, 'empImage': empImage}
        return render(request, "employeeDashboard/paySlip.html", param)

def salaryPrint(request, pk):
    if request.session.has_key('empid'):
        id = request.session['empid']
        fname = request.session['fname']
        lname = request.session['lname']
        empImage = get_object_or_404(Employee, empCode=id)
        s = get_object_or_404(monthSalary, empCode=pk)
        e1 = s.empCode
        e = Employee.objects.get(empCode=e1)
        param = {'fname': fname, 'lname': lname, 's': s, 'e': e, 'empImage': empImage}
        return render(request, "employeeDashboard/salaryPrint.html", param)

def employeeHolidays(request):
    if request.session.has_key('empid'):
        fname = request.session['fname']
        lname = request.session['lname']
        id = request.session['empid']
        empImage = get_object_or_404(Employee, empCode=id)
        h = Holidays.objects.all().order_by('-hoildayId')
        param = {'fname': fname, 'lname': lname, 'h': h, 'empImage': empImage}
        return render(request, "employeeDashboard/hoildays.html", param)


#==================Manager Dashboard ===============

def Mbase(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        return render(request, "managerDashboard/index.html", {'fname': fname, 'lname': lname})
    else:
        return render(request, "managerLogin.html")

def managerIndexPage(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
       # managerImage = request.session['img']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        t = Employee.objects.filter(managerId=id).count()
        t1 = Employee.objects.filter(managerId=id)
        p = clientProject.objects.filter(managerId=id, status='Working')
        pName = p[0].projectName
        c = client.objects.filter(managerId=id)
        cfname = c[0].fname
        clname = c[0].lname
        companyName = c[0].companyName
        companyAddress = c[0].companyAddress
        state = c[0].companyState
        img = c[0].image
        date = datetime.now().date()
        param = {'mngImage': mngImage, 'date': date, 't1': t1, 'state': state, 'companyAddress': companyAddress,
                 'companyName': companyName, 'fname': fname, 'lname': lname, 't': t, 'pName': pName,
                 'cfname': cfname, 'clname': clname, 'img':img}
        return render(request, "managerDashboard/index.html", param)
    else:
        return render(request, "managerLogin.html")

def managerTeam(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        managerId = request.session['mngid']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)

        team = Employee.objects.filter(managerId=managerId)
        return render(request, "managerDashboard/teamMembers.html", {'mngImage':mngImage, 'fname': fname, 'lname': lname, 'team':team})
    else:
        return render(request, "managerLogin.html")

def viewEmployee(request,pk):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        e = get_object_or_404(Employee, pk=pk)
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        param = {'fname': fname, 'lname': lname, 'e': e, 'mngImage': mngImage}
        return render(request, "managerDashboard/viewEmployee.html", param)
    else:
        return render(request, "managerLogin.html")

def leaveRequest(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        managerId = request.session['mngid']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        leave1 = Leave.objects.filter(managerId=managerId, status='Pending').order_by('-leaveId')
        return render(request, "managerDashboard/leaveRequest.html", {'mngImage':mngImage, 'fname': fname, 'lname': lname, 'leave': leave1})
    else:
        return render(request, "managerLogin.html")

def editLeave(request,pk):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        leave = get_object_or_404(Leave, pk=pk)
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        return render(request, "managerDashboard/editLeave.html", {'mngImage':mngImage, 'fname': fname, 'lname': lname, 'leave': leave})
    else:
        return render(request, "managerLogin.html")

def saveEditLeave(request):
    id = request.POST['id']
    status = request.POST['status']
    reason = request.POST['reason']
    leaveId = request.POST['leaveId']
    totalDays = int(request.POST['totalDays'])
    Leave.objects.filter(leaveId=leaveId).update(status=status,managerReason=reason)
    s = Employee.objects.filter(empCode=id)
    l = s[0].leave
    finalLeave = l-totalDays
    print(finalLeave)
    if request.POST['status'] == 'Approved':
        Employee.objects.filter(empCode=id).update(leave=finalLeave)
    else:
        pass
    id = request.session['mngid']
    mngImage = get_object_or_404(Manager, managerCode=id)
    return render(request, "managerDashboard/leaveRequest.html", {'mngImage':mngImage})

def leaveAccepted(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        managerId = request.session['mngid']
        leave = Leave.objects.filter(managerId= managerId, status='Approved').order_by('-leaveId')
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        param = {'fname': fname, 'lname': lname, 'leave': leave, 'mngImage':mngImage}
        return render(request, "managerDashboard/leaveAccepted.html", param)
    else:
        return render(request, "managerLogin.html")

def leaveRejected(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        managerId = request.session['mngid']
        leave = Leave.objects.filter(managerId= managerId, status='Reject').order_by('-leaveId')
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        param = {'fname': fname, 'lname': lname, 'leave': leave, 'mngImage': mngImage}
        return render(request, "managerDashboard/leaveRejected.html", param)
    else:
        return render(request, "managerLogin.html")

def employeeWorkStatus(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        managerId = request.session['mngid']
        emp = Employee.objects.filter(managerId=managerId)
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        param = {'fname': fname, 'lname': lname, 'managerId': managerId, 'emp': emp, 'mngImage':mngImage}
        return render(request, "managerDashboard/employeeWorkStatus.html", param)
    else:
        return render(request, "managerLogin.html")

def saveEmployeeWorkStatus(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        employeeId = request.POST['employeeId']
        date = request.POST['date']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        res = employeeDailyWork.objects.filter(employeeId=employeeId, date=date)
        if res:
            p = res[0].projectId
            c = res[0].clientId
            proj = clientProject.objects.filter(projectId=p)
            clt = client.objects.filter(clientId=c)
            projectName = proj[0].projectName
            cfname = clt[0].fname
            clname = clt[0].lname
            param = {'mngImage':mngImage, 'fname': fname, 'lname': lname, 'res': res, 'projectName': projectName,'cfname':cfname, 'clname':clname }
            return render(request, "managerDashboard/employeeWorkStatus.html", param)
        else:
            msg = 'No Work Status'
            param = {'fname': fname, 'lname': lname, 'msg': msg, 'mngImage':mngImage}
            return render(request, "managerDashboard/employeeWorkStatus.html", param)
    else:
        return render(request, "managerLogin.html")


def m1(request,pk):
    m = get_object_or_404(Manager, pk=pk)
    return render(request, "adminDashboard/employeeRequestView.html", {'m': m})

def profileManager(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        managerId = request.session['mngid']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        e = Manager.objects.get(managerCode=managerId)
        return render(request, "managerDashboard/profile.html", {'mngImage':mngImage,'fname': fname, 'lname': lname, 'e': e})
    else:
        return render(request, "managerLogin.html")

def saveProfile(request):
    id = request.session['mngid']
    fname = request.POST['fname']
    lname = request.POST['lname']
    phone = request.POST['phone']
    bloodGroup = request.POST['bloodGroup']
    address = request.POST['address']
    gender = request.POST['gender']
    state = request.POST['state']
    qualification = request.POST['qualification']
    emailId = request.POST['email']
    about = request.POST['about']
    e = Manager.objects.filter(managerCode=id).update(fname=fname, lname=lname, contact=phone,
         bloodGroup=bloodGroup, address=address, gender=gender, state=state,
          qualification=qualification, emailId=emailId, about=about)
    if e:
        return HttpResponseRedirect(reverse("profileManager"))
    else:
        return HttpResponse("Record Not Updated")

def projects(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        managerId = request.session['mngid']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        p = clientProject.objects.filter(managerId=managerId).order_by('-projectId')
        l = list(p)
        projectName=p[0].projectName
        projectDescription = p[0].projectDescription
        clt = p[0].clientId
        cltName = client.objects.filter(clientId=clt)
        cfname = cltName[0].fname
        clname = cltName[0].lname

        deadLine = p[0].totalDays
        param = {'l':l, 'fname': fname, 'lname': lname,'projectName':projectName, 'projectDescription': projectDescription,
                  'deadLine': deadLine, 'cfname':cfname, 'clname':clname, 'mngImage':mngImage}
        return render(request, "managerDashboard/projects.html", param)
    else:
        return render(request, "managerLogin.html")

def managerProjectView(request,pk):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        c = get_object_or_404(clientProject, pk=pk)
        projectLeader = c.managerId
        clientName = c.clientId
        m = Manager.objects.filter(managerCode=projectLeader)
        managerName = m[0].fname
        managerLname = m[0].lname
        cname = client.objects.get(clientId=clientName)
        emp = Employee.objects.filter(managerId=projectLeader)
        return render(request, 'managerDashboard/projectView.html',{'cname': cname, 'fname': fname,
        'lname': lname, 'emp': emp, 'c': c, 'managerName': managerName, 'managerLname': managerLname,
            'mngImage':mngImage})

def projectDetails(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        managerId = request.session['mngid']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        p = employeeDailyWork.objects.filter(managerId=managerId).order_by('-id')
        if p:
            n = p[0].employeeId
            pname1 = p[0].projectId
            pName = clientProject.objects.filter(projectId=pname1)
            name = Employee.objects.filter(empCode=n)
            c = p[0].clientId
            clt = client.objects.filter(clientId=c)
            param = {'fname': fname, 'lname': lname, 'managerId': managerId, 'p': p,
                     'name': name, 'pName': pName, 'clt': clt, 'mngImage':mngImage}
            return render(request, "managerDashboard/projectDetails.html", param)
        else:
            msg = 'No Project Progress'
            param = {'fname': fname, 'lname': lname, 'msg': msg, 'mngImage':mngImage}
            return render(request, "managerDashboard/projectDetails.html", param)
    else:
        return render(request, "managerLogin.html")

def projectStatusChange(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        projectStatus = request.POST['status']
        pid = request.POST['pid']
        clientProject.objects.filter(projectId=pid).update(status=projectStatus)
        param = {'fname': fname, 'lname': lname, 'mngImage':mngImage}
        return render(request, "managerDashboard/projects.html", param)
    else:
        return render(request, "managerLogin.html")

def PasswordManager(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        managerId = request.session['mngid']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        param = {'fname': fname, 'lname': lname, 'managerId': managerId, 'mngImage': mngImage}
        return render(request, "managerDashboard/changePassword.html", param)
    else:
        return render(request, "managerLogin.html")

def changePasswordManager(request):
    if request.session.has_key('mngid'):
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        managerId = request.session['mngid']
        oldPassword = request.POST['oldPassword']
        newPassword = request.POST['newPassword']
        confirmPassword = request.POST['comfirmPassword']

        oldpwd = Manager.objects.filter(managerCode=managerId)
        oldpwd[0].password
        print(oldpwd[0].password)

        if oldPassword == oldpwd[0].password:
            if newPassword == confirmPassword:
                Manager.objects.filter(managerCode=managerId).update(password=newPassword)
                msg = "Your Password Has Been Changed"
                return render(request, "managerDashboard/changePassword.html", {'msg':msg,'fname':fname, 'lname': lname, 'mngImage':mngImage})
            else:
                msg = "New Password And Confirm Password must be same"
                return render(request, "managerDashboard/changePassword.html",{'msg': msg, 'fname': fname, 'lname': lname, 'mngImage':mngImage})
        else:
            msg = "Old Password is Incorrect"
            return render(request, "managerDashboard/changePassword.html", {'msg': msg, 'fname': fname, 'lname': lname, 'mngImage':mngImage})

def addTasks(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        managerId = request.session['mngid']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        empid = Employee.objects.filter(managerId=managerId)
        projects = clientProject.objects.filter(managerId=managerId)
        param = {'fname': fname, 'lname': lname, 'managerId': managerId, 'empid': empid, 'projects':projects, 'mngImage':mngImage}
        return render(request, "managerDashboard/addTasks.html", param)
    else:
        return render(request, "managerLogin.html")

def saveAddTasks(request):
    managerId = request.session['mngid']
    clt = clientProject.objects.filter(managerId=managerId)
    cltId = clt[0].clientId
    employeeId = request.POST['empCOde']
    employeeName = request.POST['employeeName']
    managerId = request.session['mngid']
    projectName = request.POST['projects']
    document = request.FILES['document']
    date = request.POST['date']
    description = request.POST['description']
    res = tasks(employeeId=employeeId,employeeName=employeeName,managerId=managerId,projectName=projectName,
                date=date,workDescription=description,clientId=cltId, fileUpload=document)
    res.save()
    return HttpResponseRedirect(reverse(viewTasks))

def viewTasks(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        t = tasks.objects.filter(date=datetime.now().date(), managerId=id)
        param = {'fname': fname, 'lname': lname, 't': t, 'mngImage':mngImage}
        return render(request, "managerDashboard/viewTasks.html", param)
    else:
        return render(request, "managerLogin.html")

def teamAttendance(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        date = datetime.now().date()
        s = Attendance.objects.filter(date=date)
        param = {'fname': fname, 'lname': lname, 's': s, 'mngImage':mngImage}
        return render(request, "managerDashboard/teamAttendance.html", param)

    else:
        return render(request, "managerLogin.html")


def managerHolidays(request):
    if request.session.has_key('mngid'):
        fname = request.session['managerFname']
        lname = request.session['managerLname']
        id = request.session['mngid']
        mngImage = get_object_or_404(Manager, managerCode=id)
        h = Holidays.objects.all().order_by('-hoildayId')
        param = {'fname': fname, 'lname': lname, 'h': h, 'mngImage':mngImage}
        return render(request, "managerDashboard/hoildays.html", param)

    else:
        return render(request, "managerLogin.html")

'''

def logOut(request):
    del request.session['empid']
    time = datetime.now()
    empid = request.session['workId']
    employeeDailyWork.objects.filter(id=empid).update(logoutTime=time)
    Attendance.objects.filter(employeeId=empid).update(logoutTime=time)
    return redirect('index')
'''
def logOutManager(request):
    del request.session['mngid']
    return redirect('index')

def logOut(request):
    employeeId = request.session['empid']
    time = datetime.now()
    date = datetime.now().date()
    empId = request.session['workId']
    employeeDailyWork.objects.filter(id=empId).update(logoutTime=time)
    Attendance.objects.filter(employeeId=employeeId, date=date).update(logoutTime=time)

    res = employeeDailyWork.objects.filter(employeeId=employeeId, date=date)
    l = list(res)
    totalTime = 0
    if l:
        for i in l:
            id = i.id
            w = get_object_or_404(employeeDailyWork, pk=id)
            intime = w.loginTime
            inHour = intime.strftime("%H:%M:%S")
            outtime = w.logoutTime
            outHour = outtime.strftime("%H:%M:%S")
            difference = outtime - intime
            test = int(difference.total_seconds() / 60)
            print(test)
            totalTime = totalTime + test
            print("Total Time ", totalTime)
            salary = int(totalTime * 2)
            employeeDailyWork.objects.filter(id=i.id).update(duration=test, loginHour=inHour, logoutHour=outHour)
        p = perDaySalary.objects.filter(date=date, empCode=employeeId)
        if p:
            perDaySalary.objects.filter(empCode=employeeId, date=date).update(totalTime=totalTime, daySalary=salary)
        else:
            ps = perDaySalary(empCode=employeeId, date=date, totalTime=totalTime, daySalary=salary)
            ps.save()
    del request.session['empid']
    return redirect('index')

def logOutClient(request):
    del request.session['cid']
    return redirect('index')
