import multiprocessing
from sympy.ntheory import factorint

def worker():
    factorint(1239458712349817098779081798721340987234987987234, verbose=True)

if __name__ == '__main__':
    p = multiprocessing.Process(target=worker)
    p.start()

    # wait for 5 seconds or until process finishes
    p.join(5)

    if p.is_alive():
        print "still running... terminate it"

        # Terminate
        p.terminate()
        p.join()
