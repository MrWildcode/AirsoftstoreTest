from django.contrib.auth.models import User
from django.db import models



# Create your models here.
class blasters(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    manufacturer = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                              related_name='MyBlasters')
    # связь onetomany, и если пользователь удалиться - сделанные им записи останутся.
    watched = models.ManyToManyField(User, through='UserBlasterRelation',
                                      related_name='bookwatched')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)

    def __str__(self):
        return(f'ID {self.id}: {self.name}') #Чтобы в админке отображались не объекты, а норм инфа

class gear(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return(f'ID {self.id}: {self.name}') #Чтобы в админке отображались не объекты, а норм инфа

class UserBlasterRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blaster = models.ForeignKey(blasters, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_wishlist = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return (f'{self.user.username}: {self.blaster.name}, RATE {self.rate}')  # Чтобы в админке отображались не объекты, а норм инфа

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        from store.logic import set_rating
        set_rating(self.blaster)