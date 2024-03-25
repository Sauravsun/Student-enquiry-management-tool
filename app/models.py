from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers  import make_password, check_password
# Create your models here.



class enkannur(models.Model):
    fname = models.CharField(max_length=300)
    lname = models.CharField(max_length=300)
    place = models.CharField(max_length=300)
    qualification = models.CharField(max_length=300)
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=300)
    date = models.DateField(max_length=8)
    staus = models.CharField(max_length=300)
    


class knrflups(models.Model):
    date1 = models.DateField(max_length=15)
    response1 = models.CharField(max_length=200)
    enkannurfl = models.ForeignKey(enkannur, on_delete=models.CASCADE)  
 



class knrregistraion(models.Model):
    stu_id = models.AutoField(primary_key=True,unique=True,default=1001)  # Auto incrementing field starting from 1001
    knr_fname = models.CharField(max_length=300)
    knr_lname = models.CharField(max_length=300)
    knr_fathername = models.CharField(max_length=300)
    knr_mothername = models.CharField(max_length=300)
    knr_place = models.CharField(max_length=300)
    knr_qualification = models.CharField(max_length=300)
    knr_phone = models.CharField(max_length=15)
    knr_course = models.CharField(max_length=300)
    knr_coursefee = models.CharField(max_length=300)
 


class kannurpayment(models.Model):
    knrpaymentid = models.ForeignKey(knrregistraion,on_delete=models.CASCADE)
    paymentdate = models.DateField(max_length=10)
    paymentbalance = models.FloatField(max_length=100)
    paymentamount = models.FloatField(max_length=100)
    mod_payment = models.CharField(max_length=200)



#===============================================================================
#===============================================================================
#===============================================================================
    



#===============================================================================
#===============================================================================
#===============================================================================
class enkozhikode(models.Model):
    fname = models.CharField(max_length=300)
    lname = models.CharField(max_length=300)
    place = models.CharField(max_length=300)
    qualification = models.CharField(max_length=300)
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=300)
    date = models.DateField(max_length=300)
    staus = models.CharField(max_length=300)


class kozhikodeflups(models.Model):
    date1 = models.DateField(max_length=15)
    response1 = models.CharField(max_length=200)
    enkzkdfl = models.ForeignKey(enkozhikode, on_delete=models.CASCADE)  




class kzkdregistration(models.Model):
    kzstu_id = models.AutoField(primary_key=True,unique=True,default=3001)  # Auto incrementing field starting from 1001
    kz_fname = models.CharField(max_length=300)
    kz_lname = models.CharField(max_length=300)
    kz_fathername = models.CharField(max_length=300)
    kz_mothername = models.CharField(max_length=300)
    kz_place = models.CharField(max_length=300)
    kz_qualification = models.CharField(max_length=300)
    kz_phone = models.CharField(max_length=15)
    kz_course = models.CharField(max_length=300)
    kz_coursefee = models.CharField(max_length=300)


class kzkdpayment(models.Model):
    kzkdpaymentid = models.ForeignKey(kzkdregistration,on_delete=models.CASCADE)
    paymentdate = models.DateField(max_length=10)
    paymentbalance = models.FloatField(max_length=100)
    paymentamount = models.FloatField(max_length=100)
    mod_payment = models.CharField(max_length=200)

 


#===============================================================================
#===============================================================================
#===============================================================================
    



#===============================================================================
#===============================================================================
#===============================================================================
    
class enkollam(models.Model):
    fname = models.CharField(max_length=300)
    lname = models.CharField(max_length=300)
    place = models.CharField(max_length=300)
    qualification = models.CharField(max_length=300)
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=300)
    date = models.DateField(max_length=300)
    staus = models.CharField(max_length=300)


class kollmflups(models.Model):
    date1 = models.DateField(max_length=15)
    response1 = models.CharField(max_length=200)
    enkollmfl = models.ForeignKey(enkollam, on_delete=models.CASCADE)  




class kollamregistration(models.Model):
    stu_id = models.AutoField(primary_key=True,unique=True,default=2001)  # Auto incrementing field starting from 1001
    ko_fname = models.CharField(max_length=300)
    ko_lname = models.CharField(max_length=300)
    ko_fathername = models.CharField(max_length=300)
    ko_mothername = models.CharField(max_length=300)
    ko_place = models.CharField(max_length=300)
    ko_qualification = models.CharField(max_length=300)
    ko_phone = models.CharField(max_length=15)
    ko_course = models.CharField(max_length=300)
    ko_coursefee = models.CharField(max_length=300)



class kollampayment(models.Model):
    kollampaymentid = models.ForeignKey(kollamregistration,on_delete=models.CASCADE)
    paymentdate = models.DateField(max_length=10)
    paymentbalance = models.FloatField(max_length=100)
    paymentamount = models.FloatField(max_length=100)
    mod_payment = models.CharField(max_length=200)

