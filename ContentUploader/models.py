from django.db import models
from users.models import Administrator,HallManager,Customer
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from PIL import Image

# Create your models here.

class MarriageHall(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.PositiveIntegerField(null=True,blank=True)
    owner = models.ForeignKey(HallManager,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('hall-detail' , kwargs={'pk':self.pk})

    
        



class HallImages(models.Model):
    image=models.ImageField(upload_to='hall_images',default="prepared_wedding_hall.jpg")
    image_alt = models.CharField(max_length=255)
    hall=models.ForeignKey(MarriageHall,on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name
    

    # def save(self,*args,**kwargs):
    #     super().save(*args,**kwargs)  # saving image first

    #     img = Image.open(self.image.path) # Open image using self

    #     if img.height > 300 or img.width > 300:
    #         new_img = (300, 300)
    #         img.thumbnail(new_img)
    #         img.save(self.image.path)  # saving image at the same path


class HallVideos(models.Model):
    video = models.FileField(upload_to='hall_videos',null=True,validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    hall=models.ForeignKey(MarriageHall,on_delete=models.CASCADE)

    def __str__(self):
        return self.video.name


    


    
    
            