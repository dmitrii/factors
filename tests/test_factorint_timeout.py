from sympy.ntheory import factorint
import signal

def sig_handler(signum, frame):
    print "caught signal"
    raise Exception("timeout")

if __name__ == '__main__':
    signal.signal(signal.SIGALRM, sig_handler)
    signal.alarm(5)
    try:
        factorint(1239458712349817098779081798721340987234987987234, verbose=True)
    except Exception, exc:
        print exc
