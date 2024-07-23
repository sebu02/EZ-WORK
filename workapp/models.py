from django.db import models

# Create your models here.


class Login(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    usertype = models.CharField(max_length=10)


class Category(models.Model):
    name = models.CharField(max_length=30)


class Customer(models.Model):
    name = models.CharField(max_length=30)
    email=models.CharField(max_length=20)
    phone=models.CharField(max_length=10)
    photo = models.CharField(max_length=200)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)




class UserComplaint(models.Model):
    CUSTOMER = models.ForeignKey(Customer, on_delete=models.CASCADE)
    complaint=models.CharField(max_length=100)
    cdate = models.CharField(max_length=10)
    ctime = models.CharField(max_length= 10)
    reply = models.CharField(max_length= 300)
    rdate = models.CharField(max_length=10)
    rtime = models.CharField(max_length=10)


class Worker(models.Model):
    name=models.CharField(max_length=30)
    photo = models.CharField(max_length=250)
    email=models.CharField(max_length=40)
    phone=models.CharField(max_length=10)
    latitude=models.CharField(max_length=250,default=1)
    longitude=models.CharField(max_length=250,default=2)
    additionalinfo=models.CharField(max_length=100)
    models.ForeignKey(Category, on_delete=models.CASCADE)
    qualification=models.CharField(max_length=75)
    CATEGORY = models.ForeignKey(Category, on_delete=models.CASCADE)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    min_wage = models.CharField(max_length=50)

class Workerscomplaint(models.Model):
    complaint = models.CharField(max_length=100)
    WORKER = models.ForeignKey(Worker, on_delete=models.CASCADE)
    cdate = models.CharField(max_length=10)
    # ctime = models.CharField(max_length=10)
    reply = models.CharField(max_length=100)
    rdate = models.CharField(max_length=10)
    # rtime = models.CharField(max_length=10)



class feedback(models.Model):
    CUSTOMER = models.ForeignKey(Customer,default=1,on_delete=models.CASCADE)
    date = models.CharField(max_length=10)
    description = models.CharField(max_length=100)

class rating(models.Model):
    CUSTOMER = models.ForeignKey(Customer,default=1,on_delete=models.CASCADE)
    date = models.CharField(max_length=10)
    review = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    WORKER = models.ForeignKey(Worker, on_delete=models.CASCADE,default=10)


class cmp_reply(models.Model):
    description = models.CharField(max_length=100)

class schedule(models.Model):
    date=models.CharField(max_length=20)
    WORKER= models.ForeignKey(Worker, default=1, on_delete=models.CASCADE)
    status=models.CharField(max_length=20,default=1)

class Order(models.Model):
    CUSTOMER = models.ForeignKey(Customer, default=1, on_delete=models.CASCADE)
    SCHEDULE = models.ForeignKey(schedule, default=1, on_delete=models.CASCADE)
    description = models.CharField(max_length=30)
    status = models.CharField(max_length=10)
    Etime = models.CharField(max_length=10)
    amount =models.CharField(max_length=10)
    longitude =  models.CharField(max_length=50)
    latitude =  models.CharField(max_length=50)
    date =  models.CharField(max_length=50,default=1)




class payment(models.Model):
    ORDER=models.ForeignKey(Order, default=1, on_delete=models.CASCADE)
    WORKER = models.ForeignKey(Worker, default=1, on_delete=models.CASCADE)
    amount=models.CharField(max_length=10)
    time = models.CharField(max_length=10)
    status = models.CharField(max_length=20)


class blacklist(models.Model):
    WORKER = models.ForeignKey(Worker, default=1, on_delete=models.CASCADE)
    CUSTOMER = models.ForeignKey(Customer, default=1, on_delete=models.CASCADE)




