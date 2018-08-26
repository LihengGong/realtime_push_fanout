from django.db import models


# Create your models here.
class PushpinStatConn(models.Model):
    unavailable = models.BooleanField()
    conn_num = models.IntegerField()
    conn_id = models.CharField(max_length=100)
    peer_ip = models.GenericIPAddressField()
    type = models.CharField(max_length=20)

    def __str__(self):
        return "{} {} {} {} {} ".format(
            self.conn_id, self.conn_num, self.peer_ip,
            self.type, self.unavailable)


class PushpinStatReport(models.Model):
    conn_num = models.IntegerField()
    rec_msg_cnt = models.IntegerField()
    sent_msg_cnt = models.IntegerField()
    http_resp_sent_cnt = models.IntegerField()


class PushpinStatSub(models.Model):
    mode = models.CharField(max_length=20)
    channel = models.CharField(max_length=100)
    sub_cnt = models.IntegerField()
    unavailable = models.BooleanField()


class Clients(models.Model):
    channel_name = models.CharField(max_length=100)


class PushpinConnected(object):
    pass

