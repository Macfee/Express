from django.db import models

# Create your models here.

class billStatus(models.Model):
    logisticsNo = models.CharField(max_length=20)
    logisticsName = models.CharField(max_length=20)
    flag = models.CharField(max_length=1,default='0')
    user = models.CharField(max_length=20,null = True,blank=True)
    importTime = models.DateTimeField(auto_now_add=True)
    applyTime = models.DateTimeField(auto_now_add=True,null = True,blank=True)

class logistics(models.Model):
    name = models.CharField(max_length=30)
   
class Country(models.Model):
    countryCode = models.CharField(max_length=5)
    englishName = models.CharField(max_length=50)
    shortName = models.CharField(max_length=50)
    chineseName = models.CharField(max_length=50)
    commonName=models.CharField(max_length=100)
    
class Area(models.Model):

    areaNumber = models.CharField(max_length=2,null=True,blank=True)
    countryCode = models.CharField(max_length=5,null=True,blank=True)
    countryChinese = models.CharField(max_length=50,null=True,blank=True)
    channelid = models.CharField(max_length=10,null=True,blank=True)
    price = models.FloatField(max_length=10,null=True,blank=True)
  
class accountInfo(models.Model):
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    logistics = models.CharField(max_length=20)