from django.db import models
from django.contrib.auth.models import User


def default_preferences():
    return {
        "recent_users": [],
        "search_fields": []
    }


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    profile_picture = models.ImageField(default="smiling_cat.gif",
                                        upload_to="uploads/")
    middle_names = models.CharField(max_length=256, null=True)
    phone_numbers = models.CharField(max_length=256, null=True)
    room = models.CharField(max_length=256, null=True)
    search_preferences = models.JSONField(default=default_preferences)
    n_of_unread_messages = models.IntegerField(default=0)
    initialized = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    admin_pass_encrypted = models.CharField(max_length=128,
                                            null=True)

    def __str__(self):
        return self.user.username


class Hashtag(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    creator = models.ForeignKey(Profile,
                                null=True,
                                on_delete=models.SET_NULL)
    chemicals = models.ManyToManyField("chemicals.Chemical")
    n_of_chemicals = models.BigIntegerField(default=1)

    @classmethod
    def bind(cls, chemical=None, tag=None, user=None):
        if not (chemical or tag or user):
            raise ValueError(
                "All arguments must be provided: "
                "chemical, tag and user"
            )
        queryset = cls.objects.filter(name=tag)
        if len(queryset) == 0:
            hashtag = cls.objects.create(name=tag, creator=user)
        else:
            hashtag = queryset[0]
            hashtag.n_of_chemicals += 1
        hashtag.chemicals.add(chemical)

    def unbind(self, chemical):
        qset = self.chemicals.filter(id=chemical.id)
        if qset.count() == 0:
            warn("Trying to unbind hashtag from chemical "
                 "which was not bound to it")
            return None
        else:
            self.chemicals.remove(chemical)
            if self.n_of_chemicals > 1:
                self.n_of_chemicals -= 1
                self.save()
            else:
                self.delete()

    def __str__(self):
        return "#" + self.name


class Ampersandtag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    chemicals = models.ManyToManyField("chemicals.Chemical")
    n_of_chemicals = models.BigIntegerField(default=1)

    @classmethod
    def bind(cls, chemical=None, tag=None, user=None):
        if not (chemical or tag or user):
            raise ValueError(
                "All arguments must be provided: "
                "chemical, tag and user"
            )
        queryset = cls.objects.filter(name=tag, creator=user)
        if len(queryset) == 0:
            ampersandtag = cls.objects.create(name=tag, creator=user)
        else:
            ampersandtag = queryset[0]
            ampersandtag.n_of_chemicals += 1
        ampersandtag.chemicals.add(chemical)

    def unbind(self, chemical):
        qset = self.chemicals.filter(id=chemical.id)
        if qset.count() == 0:
            warn("Trying to unbind hashtag from chemical "
                 "which was not bound to it")
            return None
        else:
            self.chemicals.remove(chemical)
            if self.n_of_chemicals > 1:
                self.n_of_chemicals -= 1
                self.save()
            else:
                self.delete()

    def __str__(self):
        return "&" + self.name


class Message(models.Model):
    MOBILE = "mob"
    WEB = "web"
    EMAIL = "eml"
    MESSAGE_TYPE_CHOICES = [
        (MOBILE, "Mobile app message"),
        (WEB, "Web app message"),
        (EMAIL, "Email message"),
    ]
    id = models.BigAutoField(primary_key=True)
    header = models.CharField(max_length=32)
    content = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    time_sent = models.DateTimeField(null=True)
    message_type = models.CharField(max_length=3,
                                    choices=MESSAGE_TYPE_CHOICES,
                                    default=WEB)
    read = models.BooleanField(default=False)
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE)


class FreeBarcode(models.Model):
    number = models.BigAutoField(primary_key=True)
    standard = models.CharField(max_length=16)
