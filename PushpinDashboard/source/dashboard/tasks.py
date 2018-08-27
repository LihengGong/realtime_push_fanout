import tnetstring
import zmq
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from celery import task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import PushpinStatConn, PushpinStatSub, PushpinConnected, Clients

pushpin_connect = None


@task
def read_stats_block():
    """
    Query Pushpin's status by connecting Pushpin's ZMQ socket
    """
    # avoid launching this task multiple times
    global pushpin_connect
    if not pushpin_connect:
        pushpin_connect = PushpinConnected()
    else:
        print('already connected to Pushpin socket. Return')
        return

    print('in read_stats_block ready to connect to Pushpin socket')
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
            print(m_raw)
            m_type, m_data = m_raw.split(b' ', 1)
            print('in while loop, m_type: ', m_type)
            if len(m_data) > 1:
                process_data(m_type, m_data)
    except OSError:
        print('I/O error: {}'.format(OSError))


def process_data(m_type, m_data):
    """
    This method processes the data sent from Pushpin's socket
    """
    m_decode = tnetstring.loads(m_data[1:])
    print('in process_data: m_type=', m_type)
    print('m_decode=', m_decode)

    # If there is new data, need to notify frontend that data is updated
    if decode_data(m_decode, m_type):
        send_update_notify()


def send_update_notify():
    channel_layer = get_channel_layer()
    channel_name = None
    try:
        channel_name = Clients.objects.all()[:1].get().channel_name
    except ObjectDoesNotExist:
        print('No channels found')
    print('send_update_notify: channel_name=', channel_name)
    async_to_sync(channel_layer.send)(channel_name, {'type': 'stat.message', 'text': 'update'})


def decode_data(m_decode, m_type):
    """
    Utility method to decode pushpin status data
    :param m_decode:
    :param m_type:
    :return:
    """
    saved = False
    utf_8 = 'UTF-8'
    if m_type == b'conn':
        c_id = 'none'
        conn_num = 0
        peer_ip = '0.0.0.0'
        m_type = ''
        unavail = b'unavailable' in m_decode
        if b'id' in m_decode:
            c_id = m_decode[b'id'].decode(utf_8)
        if b'peer-address' in m_decode:
            peer_ip = m_decode[b'peer-address'].decode(utf_8)
            print('find ip address. ', peer_ip)
        if b'type' in m_decode:
            m_type = m_decode[b'type'].decode(utf_8)

        try:
            obj = PushpinStatConn.objects.get(conn_id=c_id)
            obj.conn_num = conn_num
            obj.peer_ip = peer_ip
            obj.type = m_type
            obj.unavailable = unavail
        except PushpinStatConn.DoesNotExist:
            obj = PushpinStatConn(unavailable=unavail, conn_id=c_id,
                                  conn_num=conn_num, peer_ip=peer_ip, type=m_type)
        obj.save()
        print('PushpinStatConn count: ', PushpinStatConn.objects.count())
        saved = True
    elif m_type == b'sub' or m_type == b'report' or m_type == b'activity' or m_type == b'message':
        channel = ''
        mode = ''
        sub_cnt = 0
        if b'channel' in m_decode:
            channel = m_decode[b'channel']
        if b'mode' in m_decode:
            mode = m_decode[b'mode']
        if b'subscribers' in m_decode:
            sub_cnt = m_decode[b'subscribers']
        unavailable = b'unavailable' in m_decode

        try:
            obj = PushpinStatSub.objects.get(channel=channel, mode=mode,
                                             sub_cnt=sub_cnt, unavailable=unavailable)
        except PushpinStatSub.DoesNotExist:
            obj = PushpinStatSub(channel=channel, mode=mode,
                                 sub_cnt=sub_cnt, unavailable=unavailable)
        # except MultipleObjectsReturned:
        #     PushpinStatSub.objects.filter(channel=channel, mode=mode,
        #                                   sub_cnt=sub_cnt, unavailable=unavailable)
        obj.save()
        print('PushpinStatSub count: ', PushpinStatSub.objects.count())
        saved = True
    else:
        print('not a valid type')
    return saved
