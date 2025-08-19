from django.db import models

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/')
    summary = models.TextField()
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)

class Project(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="project_images/")
    description = models.TextField()
    video = models.FileField(upload_to="project_videos/", null=True, blank=True)
    apk_url = models.FileField(upload_to="apk_files/", null=True, blank=True)

    def __str__(self):
        return self.name

class Feature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="features")
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.project.name} - {self.title}"

class SampleImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sample_images")
    image = models.ImageField(upload_to="sample_images/")

    def __str__(self):
        return f"{self.project.name} - Sample Image"    

