import time
from dgim.utils import generate_random_stream
from dgim.dgim import Dgim

def profile_dgim(dgim, stream):
    for elt in stream:
        dgim.update(elt)

def main():

    N = 100
    r = 2
    length = 1000000

    dgim = Dgim(N=N, r=r)
    stream = generate_random_stream(length=length)
    time_start = time.time()
    profile_dgim(dgim, stream)
    time_stop = time.time()
    print "Took: {}s".format(time_stop - time_start)

if __name__ == "__main__":
    main()
