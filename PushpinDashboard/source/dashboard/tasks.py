import tnetstring
import zmq
from django.conf import settings
from celery import task
from .models import PushpinStatConn, PushpinStatSub, PushpinConnected

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
    except OSError:
        print('I/O error: {}'.format(OSError))


def process_data(mtype, mdata):
    """
    This method processes the data sent from Pushpin's socket
    """
    m_decode = tnetstring.loads(mdata[1:])
    print('in process_data: mtype=', mtype)
    print('m_decode=', m_decode)

    if decode_data(m_decode, mtype):
        # need to send updated data to frontend
        pass


def decode_data(m_decode, mtype):
    saved = False
    if mtype == b'conn':
        # unavail = False
        c_id = 'none'
        conn_num = 0
        peer_ip = '0.0.0.0'
        m_type = ''
        unavail = b'unavailable' in m_decode
        if b'id' in m_decode:
            c_id = m_decode[b'id'].decode('UTF-8')
        if b'peer-address' in m_decode:
            peer_ip = m_decode[b'peer-address'].decode('UTF-8')
        if b'type' in m_decode:
            m_type = m_decode[b'type'].decode('UTF-8')
        ppstatconn = PushpinStatConn(unavailable=unavail, conn_id=c_id, conn_num=conn_num, peer_ip=peer_ip, type=m_type)
        ppstatconn.save()
        saved = True
    elif mtype == b'sub' or mtype == b'report' or mtype == b'activity' or mtype == b'message':
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
        ppstatsub = PushpinStatSub(channel=channel, mode=mode, sub_cnt=sub_cnt, unavailable=unavailable)
        ppstatsub.save()
        saved = True
    else:
        print('not a valid type')
    return saved
