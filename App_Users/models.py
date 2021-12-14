from django.db import models
from django.contrib.auth.models import User as Django_User


class OAuthRelationShip(models.Model):
    user = models.ForeignKey(Django_User, on_delete=models.CASCADE)
    open_id = models.CharField(max_length=128)
    AUTH_TYPE_CHOICES = (
        (1, 'QQ'),
        (2, 'Wechat'),
        (3, 'GitHub'),
    )
    oaurh_type = models.IntegerField(default=1, choices=AUTH_TYPE_CHOICES)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'oauthrs'
