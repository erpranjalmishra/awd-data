from django.db import models

# Create your models here.
class Sensordata(models.Model):
    id=models.AutoField(primary_key=True)
    deviceid=models.CharField(max_length=40,null=True,blank=True,default=None)
    timestamp=models.DateTimeField(auto_now_add=True)
    temp=models.FloatField()
    humidity=models.FloatField()
    phvalue=models.FloatField()
    tds=models.FloatField()
    o2=models.FloatField(null=True,blank=True,default=None)
