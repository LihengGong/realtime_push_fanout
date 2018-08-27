from django.db import models


# Create your models here.
class PushpinStatConn(models.Model):
    time_stamp = models.DateTimeField(auto_now=True)
    unavailable = models.BooleanField()
    conn_num = models.IntegerField()
    conn_id = models.CharField(max_length=100, unique=True)
    peer_ip = models.GenericIPAddressField()
    type = models.CharField(max_length=20)

    def __str__(self):
        return "time: {} id: {} conn_num: {} " \
               "peer_ip: {} type: {} unavailable: {} ".format(
                self.time_stamp, self.conn_id, self.conn_num,
                self.peer_ip, self.type, self.unavailable)

    class Meta:
        ordering = ['-time_stamp', 'conn_id']


class PushpinStatReport(models.Model):
    time_stamp = models.DateTimeField(auto_now=True)
    conn_num = models.IntegerField()
    rec_msg_cnt = models.IntegerField()
    sent_msg_cnt = models.IntegerField()
    http_resp_sent_cnt = models.IntegerField()

    def __str__(self):
        return "conn_num: {}".format(self.conn_num)

    class Meta:
        ordering = ['-time_stamp']


class PushpinStatSub(models.Model):
    time_stamp = models.DateTimeField(auto_now=True)
    mode = models.CharField(max_length=20)
    channel = models.CharField(max_length=100)
    sub_cnt = models.IntegerField()
    unavailable = models.BooleanField()

    def __str__(self):
        return "mode: {}".format(self.mode)

    class Meta:
        ordering = ['-time_stamp']


class Clients(models.Model):
    channel_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.channel_name


class PushpinConnected(object):
    pass

