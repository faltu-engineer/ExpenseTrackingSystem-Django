from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=30, default="(GMT+05:30) Chennai")
    currency = models.CharField(max_length=10, default="Rupees")
    language = models.CharField(max_length=100, default="English")
    email_confirmed = models.BooleanField(default=False)
    mobile_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def update_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
    instance.wallet.save()


class Group(models.Model):
    name = models.CharField(max_length=20, default="ETS Group")
    created_by = models.ForeignKey(to=User, on_delete=models.SET(-1))
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    group = models.ForeignKey(to=Group,on_delete=models.CASCADE , related_name='members')
    group_user = models.ForeignKey(to=User, on_delete=models.SET(-1) , related_name='member_of_groups')
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group.name


class Friend(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE , related_name='friends_to')
    friend = models.ForeignKey(to=User, on_delete=models.CASCADE , related_name='friends_by')

