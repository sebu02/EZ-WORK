import datetime

from django.db.models.expressions import RawSQL
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from workapp.models import *
from django.core.files.storage import FileSystemStorage


# syspath =r"D:\workez\workapp\static\images\\"
syspath =r"D:\latest ez work\EZ work\workez\workapp\static\images\\"
def default(request):
    data = Category.objects.all()
    return render(request,'index.html',{"data":data})
def login_post(request):
    u=request.POST["txtusername"]
    p=request.POST["txtpasswd"]

    obj = Login.objects.filter(username=u, password=p)
    if obj.exists():
        obj = obj[0]
        request.session['userid'] = obj.id
        request.session['heading'] = ""
        if obj.usertype=='admin':
            request.session['lg']='lin'
            return redirect('/admin_homepage_request')
        elif obj.usertype == 'worker':
            request.session['lg'] = 'lin'
            request.session['wid'] = Worker.objects.get(LOGIN=obj.id).id
            return redirect('/workerhome')

        else:
            return HttpResponse("<script>alert('invalid user');location='/'</script>")
    else:
        return HttpResponse("<script>alert('Username or Password is incorrect!');location='/'</script>")

#admin
def admin_homepage_request(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    return render(request, 'admin/admin_home.html')

def admin_add_category(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "Add category"
    return render(request, 'admin/categoryadd.html')
def admin_addcategory_post(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    category=request.POST["txtaddcategory"]
    if Category.objects.filter(name=category):
        return HttpResponse("<script>alert('Already added!');location='admin_add_category#contact'</script>")
    obj=Category()
    obj.name=category
    obj.save()
    return HttpResponse("<script>alert('category successfully saved');location='admin_add_category#contact'</script>")

def admin_edit_category(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    res=Category.objects.get(id=id)
    request.session['heading'] = "Edit category"
    return render(request, 'admin/categoryedit.html',{'id': id,'data':res})

def admin_edit_category_post(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "Edit category"
    category=request.POST['ctgryedit']
    q = Category.objects.filter(id=id).update(name=category)
    print(q,"")
    if q>0:
        return HttpResponse("<script>alert('category successfully saved');location='/admin_view_category#contact'</script>")
    else:
        return HttpResponse(
            "<script>alert('The Data remains unchanged.');location='/admin_view_category#contact'</script>")


def admin_delete_category(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    Category.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('category deleted successfully');location='/admin_view_category#contact'</script>")
def admin_view_category(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "View category"
    obj = Category.objects.all()
    return render(request, 'admin/categoryview.html', {"data" : obj})



def worker_approval(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    obj=Worker.objects.filter(LOGIN__usertype='pending')
    request.session['heading'] = "Verify workers"
    return render(request, 'admin/workerapproval.html',{"data":obj})


def worker_approval_post(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")

    Login.objects.filter(id=id).update(usertype='worker')
    return HttpResponse("<script>alert('approved successfully');location='/worker_approval#contact'</script>")
def worker_reject(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")

    Login.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('rejected successfully');location='/worker_approval#contact'</script>")


def worker_block_post(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")

    Login.objects.filter(id=id).update(usertype='block')
    return HttpResponse("<script>alert('approved successfully');location='/worker_view_list#contact'</script>")
def worker_unblock(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")

    Login.objects.filter(id=id).update(usertype='unblock')
    return HttpResponse("<script>alert('rejected successfully');location='/worker_view_listy#contact'</script>")


def worker_view_list(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "View workers"
    obj=Worker.objects.filter(LOGIN__usertype='worker')
    data=[]
    for i in obj:
        q=blacklist.objects.filter(WORKER=i.id)
        # if q.exists():
        #     qc = blacklist.objects.filter(WORKER=i.id).count()
        #
        #     data.append(
        #         {
        #            "id":i.id,
        #             "count": qc,
        #             "photo": i.photo,
        #
        #             "name":i.name,
        #             "email":i.email,
        #             "phone":i.phone,
        #             "CATEGORY":i.CATEGORY,
        #             "qualification":i.qualification,
        #             "additionalinfo":i.additionalinfo,
        #             "min_wage":i.min_wage,
        #
        #         }
        #     )
        data.append(
            {
                "id": i.id,
                "count": '0',
                "photo": i.photo,
                "name": i.name,
                "email": i.email,
                "phone": i.phone,
                "CATEGORY": i.CATEGORY,
                "qualification": i.qualification,
                "additionalinfo": i.additionalinfo,
                "min_wage": i.min_wage,
                "latitude": i.latitude,
                "longitude": i.longitude,


        }
        )
    return render(request, 'admin/workerview.html',{"data":data})
def workerblacklist(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "Black List"
    obj=Worker.objects.filter(LOGIN__usertype='worker')
    data=[]
    for i in obj:
        q=blacklist.objects.filter(WORKER=i.id)
        if q.exists():
            qc = blacklist.objects.filter(WORKER=i.id).count()


            data.append(
                {
                   "id":i.id,
                    "count": qc,
                    "photo": i.photo,

                    "name":i.name,
                    "email":i.email,
                    "phone":i.phone,
                    "CATEGORY":i.CATEGORY,
                    "qualification":i.qualification,
                    "additionalinfo":i.additionalinfo,
                    "min_wage":i.min_wage,

                }
            )
    return render(request, 'admin/workerblacklist.html', {"data": data})
def blacklistdelete(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")

    Login.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('removed successfully');location='/workerblacklist#contact'</script>")


def admin_view_customer(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "View customer"
    obj = Customer.objects.all()
    return render(request, 'admin/customerview.html',{"data":obj})



def user_view_complaint(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "View complaints"
    obj= UserComplaint.objects.all()
    return render(request, 'admin/customerreply.html',{"data":obj})
def worker_view_complaint(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "View complaints"
    obj=Workerscomplaint.objects.all()
    return render(request, 'admin/workerreply.html',{"data":obj})
def cmp_reply(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "Send reply"
    return render(request, 'admin/cmpreply.html',{'id':id})
def  cmp_replypost(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    reply=request.POST["reply"]
    d=datetime.datetime.now().strftime("%Y-%m-%d")
    t=datetime.datetime.now().strftime("%H:%M:%S")
    UserComplaint.objects.filter(id=id).update(reply=reply,rdate=d,rtime=t)
    return HttpResponse("<script>alert('replied');location='/user_view_complaint#contact'</script>")

def cmp_replyy(request,id):
    request.session['heading'] = "Send reply"
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    return render(request, 'admin/cmpreply2.html',{'id':id})
def  cmp_replyypost(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")

    reply=request.POST["reply"]
    d=datetime.datetime.now().strftime("%Y-%m-%d")
    t=datetime.datetime.now().strftime("%H-%M-%S")
    Workerscomplaint.objects.filter(id=id).update(reply=reply,rdate=d)
    return HttpResponse("<script>alert('replied');location='/worker_view_complaint#contact'</script>")

def feedback_view_request(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "View feedback"
    ref=feedback.objects.all()
    return render(request, 'admin/feedbackview.html',{'data':ref})


def rating_view_request(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "View rating"
    ref=rating.objects.filter(WORKER=id)
    return render(request, 'admin/workerreview.html',{'data':ref})


def admin_changepass_request(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "Change password"
    return render(request, 'admin/changepassadd.html')
def admin_changepass_post(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")

    cp=request.POST['textfield']
    np=request.POST['textfield2']
    pp=request.POST['textfield3']
    ref=Login.objects.filter(password=cp)
    if ref.exists():
        if (np==pp):
            q = Login.objects.filter(usertype='admin').update(password=pp)
            if int(q)>0:
                return HttpResponse("<script>alert('password changed');location='/'</script>")
            else:
                return HttpResponse("<script>alert('The password remains unchanged.');location='/admin_changepass_request#contact'</script>")
        else:
            return HttpResponse("<script>alert('password mismatched');location='/admin_changepass_request#contact'</script>")
    else:
        return HttpResponse("<script>alert('current password mismatched');location='/admin_changepass_request#contact'</script>")


def logout(request):
    request.session['lg']=""
    request.session['heading'] = ""
    return redirect('/')


#worker


def workeradd(request):

    data=Category.objects.all()
    return render(request,'worker/workeradd.html',{'data':data})

def workeraddpost(request):

    u = request.POST["useremail"]
    p = request.POST["userpasswd"]
    c=request.POST["cnf"]
    name= request.POST["txtname"]
    email= request.POST["useremail"]
    # address=request.POST["address"]
    additinfo=request.POST["addinfo"]
    ctgry=request.POST["ctgry"]
    phone= request.POST["phone"]
    Quali=request.POST["Quali"]
    global path
    try:
        photo=request.FILES["photo"]
        date=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        fs=FileSystemStorage()
        fs.save(syspath +date +'.jpg',photo)
        path="/static/images/"+ date +'.jpg'
    except Exception as e:
        print(e)
        path="/static/a.jfif"

    print(path,"gkgjgkjf")
    minw=request.POST["minw"]
    if Login.objects.filter(username=email).exists():
        return HttpResponse("<script>alert('Email already exists');location='/'</script>")
    obj=Login()
    obj.username=email
    obj.usertype = "pending"
    if p == c:
        obj.password = p
        obj.save()
    else:
        return HttpResponse("<script>alert('password does not match');location='/'</script>")

    obj2=Worker()

    obj2.name=name
    obj2.email=email
    obj2.CATEGORY_id=ctgry
    obj2.qualification=Quali
    obj2.photo=path
    obj2.longitude=request.POST['lg']
    obj2.latitude=request.POST['lt']
    obj2.additionalinfo=additinfo
    obj2.min_wage=minw
    obj2.phone=phone
    obj2.LOGIN=obj
    obj2.save()

    return HttpResponse("<script>alert('your request has been send');location='/'</script>")


#workerhomepage
def workerhome(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")

    return render(request,"worker/workerhomepage.html")

def workerprofileview(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "My Profile"
    userid=request.session['userid']
    res = Worker.objects.get(LOGIN_id=userid)

    return render(request,"worker/workernewprofileview.html",{"i":res })

def workerprofileedit(request,id):
    request.session['heading'] = "Update profile"
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    # userid = request.session['userid']
    res = Worker.objects.get(id=id)
    obj=Category.objects.all()


    return render(request,"worker/workeredit.html",{"data":res ,'id':id ,"cat":obj})


def workerprofileedit_post(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    try:
        name = request.POST["txtname1"]
        email = request.POST["useremail"]
        ctgry = request.POST["ctgry"]
        longitude = request.POST['lg']
        latitude = request.POST['lt']
        additinfo = request.POST["addinfo"]
        phone = request.POST["phone"]
        Quali = request.POST["Quali"]
        photo=request.FILES["photo"]
        date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        fs = FileSystemStorage()
        fs.save(syspath + date + '.jpg', photo)
        path = "/static/images/" + date + '.jpg'
        minw = request.POST["minw"]
        Worker.objects.filter(id=id).update(longitude = request.POST['lg'],latitude = request.POST['lt'],name=name,email=email,CATEGORY_id=ctgry,photo=path,qualification=Quali,min_wage=minw,phone=phone,additionalinfo=additinfo)
        return HttpResponse("<script>alert('profile updated');location='/workerprofileview#contact'</script>")
    except Exception as e:
        name = request.POST["txtname1"]
        email = request.POST["useremail"]
        ctgry = request.POST["ctgry"]
        additinfo = request.POST["addinfo"]
        phone = request.POST["phone"]
        Quali = request.POST["Quali"]
        minw = request.POST["minw"]
        Worker.objects.filter(id=id).update(longitude = request.POST['lg'],latitude = request.POST['lt'],name=name, email=email, CATEGORY_id=ctgry,
                                            min_wage=minw, phone=phone, additionalinfo=additinfo,qualification=Quali)
        return HttpResponse("<script>alert('profile updated');location='/workerprofileview#contact'</script>")

def workerscheduleadd(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "Add schedule"
    d = int(datetime.datetime.now().strftime("%d"))+1
    d2 = str(datetime.datetime.now().strftime("%Y"))+'-'+str(datetime.datetime.now().strftime("%m"))+'-0'+str(d)
    print(d2)
    return render(request,"worker/workerscheduleadd.html",{"data":d2})

def workerscheduleadd_post(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "Add schedule"
    if schedule.objects.filter(date = request.POST['sdate'],WORKER_id = request.session['wid']).exists():
        return HttpResponse(
            "<script>alert('Schedule already added....');location='/workerschedule#contact'</script>")

    obj = schedule()
    obj.date = request.POST['sdate']
    obj.WORKER_id = request.session['wid']
    obj.save()
    return HttpResponse(
        "<script>alert('Schedule added successfully....');location='/workerschedule#contact'</script>")


def workerschedule(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "View schedule"
    obj=schedule.objects.filter(WORKER=request.session['wid'])
    return render(request,"worker/workerschedule.html",{'data':obj})

def wrker_delete_schedule(request,id):
    schedule.objects.get(id=id).delete()
    return HttpResponse(
        "<script>alert('Schedule deleted successfully....');location='/workerschedule#contact'</script>")


def workrequest(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "My request"
    obj = Order.objects.filter(status='pending',SCHEDULE__WORKER=request.session['wid'])
    return render(request,"worker/workerworkrequest.html",{"data":obj})


def workrequestaccept(request, id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "Work estimations"
    userid = request.session['userid']
    res = Worker.objects.get(LOGIN_id=userid).min_wage
    return render(request, 'worker/workerworkestimation.html', {"rid": id,"a":res})

def workrequestaccept_post(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    eamount=request.POST['txtpayment']
    etime=request.POST['txttime']
    Order.objects.filter(id=id).update(status='Approved',amount=eamount,Etime=etime )
    return HttpResponse("<script>alert('approved successfully');location='/workrequest#contact'</script>")

def workreject_post(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    Order.objects.filter(id=id).update(status='Rejected')
    return HttpResponse("<script>alert('rejected successfully');location='/workrequest'</script>")



def orderstatus(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "My booking"
    obj=Order.objects.filter(status='Approved',SCHEDULE__WORKER=request.session['wid'])
    return render(request,"worker/workerorderstatus.html",{"data":obj})


def todaysbooking(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "Today's booking"
    obj=Order.objects.filter(status='Approved',SCHEDULE__WORKER=request.session['wid'],SCHEDULE__date=datetime.datetime.now().date())
    return render(request,"worker/workertodaysorder.html",{"data":obj})

def schedulebooking(request,id):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")

    obj=Order.objects.filter(status='Approved',SCHEDULE=id,SCHEDULE__date=datetime.datetime.now().date())
    request.session['heading'] =  "Booking for "+str(obj[0].SCHEDULE.date)
    return render(request,"worker/workertodaysorder.html",{"data":obj})

def wcomplaint(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "Send complaint"
    return render(request,"worker/workercomplaintadd.html")
def wcomplaint_post(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    cmp=request.POST["txtcmp"]
    wid = Worker.objects.get(LOGIN_id=request.session['userid'])
    d=datetime.datetime.now().strftime("%Y-%m-%d")
    obj=Workerscomplaint()
    obj.cdate=d
    obj.complaint=cmp
    obj.reply='pending'
    obj.rdate='pending'
    obj.WORKER = wid
    obj.save()
    return HttpResponse("<script>alert('complaint registered');location='/workerhome'</script>")

def workercmpreply(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "View complaint"
    obj=Workerscomplaint.objects.filter(WORKER=request.session['wid'])
    return render(request,"worker/workercomplaintreply.html",{"data":obj})


def wreview(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    request.session['heading'] = "View review"
    obj=rating.objects.filter(WORKER=request.session['wid'])
    return render(request,"worker/workerrating.html",{"data":obj})

def worker_changepass_request(request):
    request.session['heading'] = "Change password"
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    return render(request, 'worker/workerchangepass.html')

def worker_changepass_post(request):
    if request.session['lg'] != 'lin':
        return HttpResponse("<script>alert('please login!');location='/'</script>")
    cp=request.POST['wpass']
    np=request.POST['wnpass']
    pp=request.POST['wcpass']
    ref=Login.objects.filter(password=cp,id= request.session['userid'])
    if ref.exists():
        if np==pp:
            q=Login.objects.filter(id= request.session['userid']).update(password=pp)
            if int(q)>0:
                return HttpResponse("<script>alert('password changed');location='/'</script>")
            else:
                return HttpResponse(
                    "<script>alert('The password remains unchanged.');location='/worker_changepass_request#contact'</script>")
        else:
            return HttpResponse("<script>alert('password mismatched');location='/worker_changepass_request#contact'</script>")
    else:
        return HttpResponse("<script>alert('current password mismatched');location='/worker_changepass_request#contact'</script>")

# =================================================
def and_login(request):
    uname=request.POST['username']
    p=request.POST['password']
    obj = Login.objects.filter(username=uname, password=p)
    if obj.exists():
        lid=obj[0].id
        print("liddd",lid)
        type=obj[0].usertype
        print("type",type)
        return JsonResponse({"status":"ok",'lid':lid,'type':type})
    else:
        return JsonResponse({'status':"none"})

def customer_registration(request):
    name=request.POST["name"]
    phone=request.POST["phone"]
    email=request.POST["email"]
    print(name)

    password= request.POST["pass"]

    pic=request.FILES["pic"]
    date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    fs = FileSystemStorage()
    fs.save(syspath + date + '.jpg', pic)
    path = "/static/images/" + date + '.jpg'
    obj1=Login()
    obj1.username=email
    obj1.password=password
    obj1.usertype="customer"
    obj1.save()
    obj=Customer()
    obj.name=name
    obj.phone=phone
    obj.email=email

    obj.photo=path
    obj.LOGIN=obj1
    obj.save()
    return JsonResponse({"status":"ok"})


def customer_changepass(request):
    currentpass=request.POST["cp"]
    newpass = request.POST["np"]
    confirm = request.POST["cnf"]
    lid = request.POST["lid"]
    ref = Login.objects.filter(password=currentpass, id=lid)
    if ref.exists():
        if newpass == confirm:
            q = Login.objects.filter(id=lid).update(password=confirm)
            return JsonResponse({'status': "ok"})

        else:
                return JsonResponse({'status': "missmatch"})
    else:
      return JsonResponse({'status': "ok"})

def Complaint(request):
    complaint=request.POST["cmp"]
    lid = request.POST["lid"]

    obj = UserComplaint()
    obj.complaint=complaint
    obj.CUSTOMER=Customer.objects.get(LOGIN=lid)
    obj.cdate=datetime.datetime.now().strftime("%Y-%m-%d")
    obj.ctimee=datetime.datetime.now().strftime("%H:%M:%S")
    obj.reply="pending"
    obj.rdate="pending"
    obj.rtime="pending"
    obj.save()

    return JsonResponse({'status': "ok"})


def and_feedback(request):
    feed=request.POST["feedback"]
    lid = request.POST["lid"]

    obj = feedback()
    obj.description=feed
    obj.CUSTOMER = Customer.objects.get(LOGIN=lid)
    obj.date = datetime.datetime.now().strftime("%Y-%m-%d")
    obj.save()
    return JsonResponse({'status': "ok"})

def view_profile(request):
    lid=request.POST["lid"]
    obj=Customer.objects.get(LOGIN=lid)
    return JsonResponse({'status':"ok","name":obj.name,"email":obj.email,"phone":obj.phone,"photo":obj.photo})
def viewlistworker(request):
    wid=request.POST["wid"]

    i=Worker.objects.get(id=wid)

    return JsonResponse({'status': "ok",

                "cat": i.CATEGORY.name,
                "name": i.name,
                "bio": i.additionalinfo,
                "quali": i.qualification,
                "phone": i.phone,
                "minwage": i.min_wage,
                 "img1": i.photo,
                 "latitude": i.latitude,
                 "longitude": i.longitude,

               })

def booking (request):
    des=request.POST["descrption"]
    lid = request.POST["lid"]
    wid=request.POST["wid"]
    lat=request.POST["lat"]
    log=request.POST["logi"]
    qry1=Order.objects.filter(SCHEDULE__WORKER=wid,CUSTOMER__LOGIN=lid,status="pending")
    if qry1.exists():
        return JsonResponse({"status":"oky"})
    else:
        qry=schedule.objects.filter(WORKER=wid).order_by("-id")
        if qry.exists():
            obj = Order()
            obj.description = des
            obj.CUSTOMER = Customer.objects.get(LOGIN=lid)
            obj.SCHEDULE_id=qry[0].id
            obj.status="pending"
            obj.Etime=datetime.datetime.now().strftime("%H:%M:%S")
            obj.amount="0"
            obj.date=datetime.datetime.now().strftime("%Y-%m-%d")
            obj.latitude=lat
            obj.longitude=log
            obj.save()
            return JsonResponse({'status': "ok"})
        else:
            return JsonResponse({"status":"no"})

def Viewrequest(request):
    lid = request.POST["lid"]
    obj = Order.objects.filter(CUSTOMER__LOGIN=lid)
    ar = []
    for i in obj:
        ar.append(
            {
                "id": i.id,
                "photo": i.SCHEDULE.WORKER.photo,
                "CATEGORY_id": i.SCHEDULE.WORKER.CATEGORY.name,
                "name": i.SCHEDULE.WORKER.name,
                 "description": i.description,
                "status": i.status,
                 "email": i.SCHEDULE.WORKER.email,
                "phone": i.SCHEDULE.WORKER.phone,
                "min_wage": i.SCHEDULE.WORKER.min_wage,
                "amount": i.amount,
                 "Etime": i.Etime,
                "lat":i.latitude,
                "log":i.longitude,
                "wid":i.SCHEDULE.WORKER.id


            }
        )
    return JsonResponse({'status': "ok", "data": ar})
def cancelrequest(request):
    oid=request.POST['id']
    Order.objects.filter(id=oid).delete()
    return JsonResponse({'status': "ok"})
def sendrating(request):
    review = request.POST["review"]
    r = request.POST["r"]
    lid = request.POST["lid"]
    wid = request.POST["wid"]

    obj = rating()
    obj.rating=r
    obj.review=review
    obj.WORKER_id=wid
    obj.date = datetime.datetime.now().strftime("%Y-%m-%d")

    obj.CUSTOMER = Customer.objects.get(LOGIN=lid)
    obj.save()
    return JsonResponse({'status': "ok"})
def customer_profile_update(request):
    lid = request.POST["lid"]
    name = request.POST["name"]
    phone = request.POST["phone"]

    print(name)



    pic = request.FILES["pic"]
    date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    fs = FileSystemStorage()
    fs.save(syspath + date + '.jpg', pic)
    path = "/static/images/" + date + '.jpg'
    Customer.objects.filter(LOGIN=lid).update(name=name,phone=phone)
    return JsonResponse({'status': "ok"})


def shortview(request):
    # obj = Worker.objects.all()
    latitude = request.POST['lat']
    longitude = request.POST['log']

    ###### NEAR-BY code

    gcd_formula = "6371 * acos(least(greatest(cos(radians(%s)) * cos(radians('" + latitude + "')) * cos(radians('" + longitude + "') - radians(%s)) + sin(radians(%s)) * sin(radians('" + latitude + "')), -1), 1))"
    print(gcd_formula)
    distance_raw_sql = RawSQL(
        gcd_formula, (latitude, longitude, latitude)
    )
    qry = Worker.objects.filter(LOGIN__usertype="worker")
    li = []
    for i in qry:
        qs = Worker.objects.filter(id=i.id).annotate(
            distance=RawSQL(gcd_formula, (i.latitude, i.longitude, i.latitude))).order_by('distance')
        li.append({
            "id": i.id,
                    "img": i.photo,
                    "name": i.name,

                    "phone": i.phone,
                    "minwage": i.min_wage,
                    "cat": i.CATEGORY.name,
                    "log": i.latitude,
                    "lat": i.longitude,
                    "r": '0',
            "Hospital_distance": qs[0].distance
        })
        print("li",li)


    #### Distance arranging.........................

    def hospital_nearby_sort(e):
        return e['Hospital_distance']

    li.sort(key=hospital_nearby_sort)
    # print("hhhhh",li[0:6])
    # for i in li[0:6]:
    #     print(i)

    # ar = []
    # for i in obj:
    #     qry=rating.objects.filter(WORKER=i.id)
    #     if qry.exists():
    #         # rr=rating.objects.filter(WORKER=i.id).avg(rating)
    #         # print(rr)
    #         ar.append(
    #             {
    #                 "id": i.id,
    #                 "img": i.photo,
    #                 "name": i.name,
    #
    #                 "phone": i.phone,
    #                 "minwage": i.min_wage,
    #                 "cat": i.CATEGORY.name,
    #                 "log": i.latitude,
    #                 "lat": i.longitude,
    #                 "r": '0'
    #             }
    #         )
    #     ar.append(
    #         {
    #             "id": i.id,
    #             "img": i.photo,
    #             "name": i.name,
    #
    #             "phone": i.phone,
    #             "minwage": i.min_wage,
    #             "cat": i.CATEGORY.name,
    #             "log": i.latitude,
    #             "lat": i.longitude,
    #             "r": '0'
    #
    #         }
    #     )
    return JsonResponse({'status': "ok", "data": li})

def view_schedule(request):
    wid=request.POST['wid']
    obj=schedule.objects.filter(WORKER=wid)
    ar=[]
    for i in obj:
        ar.append(
            {
                "id":i.id,
                "date":i.date
            }
        )

    return JsonResponse({'status': "ok", "data": ar})


def customhome(request):
    # obj = Worker.objects.all()
    latitude = request.POST['lat']
    longitude = request.POST['log']

    ###### NEAR-BY code

    gcd_formula = "6371 * acos(least(greatest(cos(radians(%s)) * cos(radians('" + latitude + "')) * cos(radians('" + longitude + "') - radians(%s)) + sin(radians(%s)) * sin(radians('" + latitude + "')), -1), 1))"
    print(gcd_formula)
    distance_raw_sql = RawSQL(
        gcd_formula, (latitude, longitude, latitude)
    )
    qry = Worker.objects.filter(LOGIN__usertype="worker")
    li = []
    for i in qry:
        qs = Worker.objects.filter(id=i.id).annotate(
            distance=RawSQL(gcd_formula, (i.latitude, i.longitude, i.latitude))).order_by('distance')
        li.append({
            "id": i.id,
            "img": i.photo,
            "name": i.name,

            "phone": i.phone,
            "minwage": i.min_wage,
            "cat": i.CATEGORY.name,
            "log": i.latitude,
            "lat": i.longitude,
            "r": '0',
            "Hospital_distance": qs[0].distance
        })
    return JsonResponse({"status":"ok","data":li})


def and_blacklist(request):
    id=request.POST['id']
    lid=request.POST['lid']
    q=Order.objects.get(id=id)
    wid=q.SCHEDULE.WORKER_id
    obj=blacklist()
    obj.WORKER_id=wid
    obj.CUSTOMER=Customer.objects.get(LOGIN=lid)
    obj.save()
    return JsonResponse({"status":"ok"})


























































