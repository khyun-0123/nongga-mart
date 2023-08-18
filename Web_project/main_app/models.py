from django.db import models

# Create your models here.

class post_data_model(models.Model):
    Post_ID_field=models.IntegerField(unique=True)
    title_field=models.CharField(max_length=100)
    content_field=models.CharField(max_length=200)
    User_ID_field=models.CharField( max_length=50)
    Time_field=models.DateTimeField()