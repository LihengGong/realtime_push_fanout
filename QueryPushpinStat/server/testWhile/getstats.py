import socket
import tnetstring
import zmq
from django.conf import settings
from .models import PushpinStat_Conn, PushpinStat_Sub, PushpinConnected
from .postpone import postpone

pushpin_connect = None


@postpone
def read_stats_block():
    """
    Query Pushpin's status by connecting Pushpin's ZMQ socket
    """
    # TODO: although this task has been "backgrounded", we still
    # need to add some kind of check to avoid lauching this task
    # multiple times
    global pushpin_connect
    if not pushpin_connect:
        pushpin_connect = PushpinConnected()
    else:
        print('already connected to Pushpin socket. Return')
        return
    print('in getstats ready to connect to Pushpin socket')
    sock_file = settings.PUSHPIN_SOCKET_FILE
    print('sock_file is: ', sock_file)
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    sock.connect(sock_file)
    sock.setsockopt(zmq.SUBSCRIBE, b"")
    print('before while loop')

    try:
        while True:
            m_raw = sock.recv()
            mtype, mdata = m_raw.split(b' ', 1)
            print('in while loop, mtype: ', mtype)
            if len(mdata) > 1:
                process_data(mtype, mdata)
    except socket.error:
        print('I/O error: ', ose)


"""
class PushpinStat_Conn(models.Model):
    unavailable = models.BooleanField()
    # fromwhich = models.CharField(max_length=100)
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
"""


def process_data(mtype, mdata):
    """
    This method processes the data sent from Pushpin's socket
    """
    mdecode = tnetstring.loads(mdata[1:])
    print('in process_data: mtype=', mtype)
    print('mdecode=', mdecode)
    if mtype == b'conn':
        # unavail = False
        c_id = 'none'
        conn_num = 0
        peer_ip = '0.0.0.0'
        unavail = b'unavailable' in mdecode
        if b'id' in mdecode:
            c_id = mdecode[b'id'].decode('UTF-8')
        ppstatconn = PushpinStat_Conn(unavailable=unavail, conn_id=c_id, conn_num=conn_num, peer_ip=peer_ip, type='ws')
        ppstatconn.save()
    elif mtype == b'sub' or mtype == b'report' or mtype == b'activity' or mtype == b'message':
        channel = ''
        mode = ''
        sub_cnt = 0
        if b'channel' in mdecode:
            channel = mdecode[b'channel']
        if b'mode' in mdecode:
            mode = mdecode[b'mode']
        if b'subscribers' in mdecode:
            sub_cnt = mdecode[b'subscribers']
        unavailable = b'unavailable' in mdecode
        ppstatsub = PushpinStat_Sub(channel=channel, mode=mode, sub_cnt=sub_cnt, unavailable=unavailable)
        ppstatsub.save()
    else:
        print('not a valid type')
