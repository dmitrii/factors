from sympy.ntheory import factorint
import signal
import time

def sig_handler(signum, frame):
    print "caught signal"
    raise Exception("timeout")

if __name__ == '__main__':
    N = 1239458712349817098779081798721340987234987987234

    signal.signal(signal.SIGALRM, sig_handler)
    l = 1
    while l <= 10000000: # at 10M, the big numbers seem to take longer than 2min and more than 3GB of memory
        signal.alarm(120) # cancels previous alarm
        start_time = time.time()
        try:
            factors = factorint(N, limit=l, verbose=False)
        except Exception, exc:
            print exc
        print "limit=" + str(l) + " elapsed: " + str(time.time() - start_time) + " result: " + str(factors)
        l *= 10
