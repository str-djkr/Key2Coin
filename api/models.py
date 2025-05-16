from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    total_keystrokes = models.PositiveIntegerField(default=0)
    total_coins = models.FloatField(default=0.0)
    current_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(default=timezone.now)

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'

    def __str__(self):
        return self.username

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    date = models.DateField(default=timezone.now)
    keystrokes = models.PositiveIntegerField(default=0)
    coins_earned = models.FloatField(default=0.0)
    source_app = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "User Activities"
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"{self.user.username}: {self.keystrokes} keystrokes on {self.date}"

class LandingPage(models.Model):
    title = models.CharField(max_length=200, default="Key2Coin")
    description = models.TextField(default="Turn your keystrokes into crypto rewards!")
    iframe_url = models.URLField(blank=True, null=True, help_text="URL for iframe embedding")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

@receiver(post_save, sender=User)
def create_initial_activity(sender, instance, created, **kwargs):
    if created:
        UserActivity.objects.create(user=instance)