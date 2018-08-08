from django.db import models


# Create your models here.
class PushpinStat_Conn(models.Model):
    unavailable = models.BooleanField()
    conn_num = models.IntegerField()
    conn_id = models.CharField(max_length=100)
    peer_ip = models.GenericIPAddressField()
    type = models.CharField(max_length=20)


class PushpinStat_Report(models.Model):
    conn_num = models.IntegerField()
    rec_msg_cnt = models.IntegerField()
    sent_msg_cnt = models.IntegerField()
    http_resp_sent_cnt = models.IntegerField()


class PushpinStat_Sub(models.Model):
    mode = models.CharField(max_length=20)
    channel = models.CharField(max_length=100)
    sub_cnt = models.IntegerField()
    unavailable = models.BooleanField()


class PushpinConnected(object):
    pass
