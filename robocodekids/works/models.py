from django.db import models
from account.models import User
from django.urls import reverse


class Work(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=55)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=400)
    image = models.ImageField(upload_to='work/images/%y/%m/%d/')
    to_work = models.URLField(max_length=200)
    likes = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.created_at} - {self.author}'

    def get_absolute_url(self):
        return reverse('work:project-detail', kwargs={'slug': self.slug})


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    work = models.ForeignKey(Work, on_delete=models.PROTECT)
    created_at = models.DateField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     self.work.likes_count += 1
    #     self.work.save()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Like to {self.work} from {self.user}"


class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Viewed to {self.work} from {self.user}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"{self.name}"


class Banner(models.Model):
    image = models.ImageField('Banner rasmi', upload_to='banner/image-%y-%m-%d/')
    title = models.CharField('Sarlavha', max_length=255)
    description = models.TextField('Malumot')
    to_url = models.URLField('Manzil')

    def __str__(self):
        return f"{self.title}"
