from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

from game.models import Game


class MyUserManager(BaseUserManager):
    def create_user(self, username, name, age, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(username=username, Name=name, Age=age)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, Name, Age, password=None):
        """
        Creates and saves a superuser with the given username, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,
            name=Name,
            age=Age,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # UId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=255, null=True)
    Age = models.IntegerField(null=True)
    Owns = models.ManyToManyField(Game, related_name="game_own", blank=True)
    Favorites = models.ManyToManyField(Game, related_name="game_favorites", blank=True)

    # Default user fields
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True)

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["Name", "Age"]

    def __str__(self):
        return self.Name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def favorite_game(self, game_id: str):
        self.Favorites.add(Game.objects.get(GameId=game_id))
        self.save()

    def own_game(self, game_id: str):
        self.Owns.add(Game.objects.get(GameId=game_id))
        self.save()
