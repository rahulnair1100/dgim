import itertools
import math

class Dgim(object):
    """An implementation of the DGIM algorithm.
    It estimates the number of 1s present in a sliding window of a stream
    while using few memory.

    The algorithm is described in:
    Datar, Mayur, et al. "Maintaining stream statistics over sliding windows."
    SIAM Journal on Computing 31.6 (2002): 1794-1813.

    An explanation of the algorithm can also be found here:
    http://infolab.stanford.edu/~ullman/mmds/ch4.pdf
    """

    def __init__(self, N, r=2):
        """Constructor
        :param N: size of the sliding window
        :type N: int
        :param r: the maximum number of buckets of the same size
        :type r: int
        """
        self.N = N
        if r < 2:
            raise ValueError("'r' should be higher or equal to 2. Got {}.".format(r))
        self.r = r
        self.buckets = []
        self.timestamp = 0

    @property
    def error_rate(self):
        """Return the maximum error rate made by the algorithm.
        Let c be the true result and e the estimate returned by the dgim
        algorithm.
        abs(c-e) < error_rate * c
        :returns: float
        """
        return 1/float(self.r)

    def update(self, elt):
        """Update the stream with one element.
        The element can be either 0 or 1.
        :param elt: the latest element of the stream
        :type elt: int
        """
        self.timestamp += 1
        #check if oldest bucket should be removed
        if (len(self.buckets) > 0 and
                self.buckets[-1].most_recent_timestamp <= self.timestamp - self.N):
            self.buckets = self.buckets[:-1]
        if elt != 1:
            return
        reminder = Bucket(self.timestamp, 1)
        buckets = []
        new_buckets_len = 0
        for k, crt_buckets in itertools.groupby(self.buckets, key=lambda x: x.one_count):
            old_buckets_len = new_buckets_len
            if reminder is not None:
                buckets.append(reminder)
                reminder = None
            for bucket in crt_buckets:
                buckets.append(bucket)

            new_buckets_len = len(buckets)
            if new_buckets_len - old_buckets_len == self.r + 1:
                last = buckets.pop()
                last_previous = buckets.pop()
                last_previous.merge(last)
                reminder = last_previous
        if reminder is not None:
            buckets.append(reminder)
        self.buckets = buckets

    def get_count(self):
        """Returns an estimate of the number of ones in the sliding window.
        :returns: int
        """
        #find the all the buckets which most recent timestamp is ok
        result = 0
        value = 0
        min_timestamp = self.timestamp - self.N
        for bucket in self.buckets:
            #break once we have found an old bucket
            if bucket.most_recent_timestamp <= min_timestamp:
                break
            value = bucket.one_count
            result += value
        #remove half the value of the last processed bucket.
        result -= math.floor(value/2)
        return result


class Bucket(object):
    """A class to represent a bucket."""
    def __init__(self, most_recent_timestamp, one_count):
        """Constructor
        :param most_recent_timestamp: the timestamp of the most recent element
                                      that belongs to the bucket.
        :type most_recent_timestamp: int
        :param one_count: the count of ones in this bucket.
                          It must be a power of 2.
        """
        self.most_recent_timestamp = most_recent_timestamp
        self.one_count = one_count

    def merge(self, other_bucket):
        """Merge this bucket with an other bucket.
        :param other_bucket: the bucket that has to be merged with this one.
        :type other_bucket: Bucket
        """
        self.most_recent_timestamp = max(
                self.most_recent_timestamp,
                other_bucket.most_recent_timestamp)
        self.one_count += other_bucket.one_count

    def __repr__(self):
        return "Bucket {}: {}".format(self.most_recent_timestamp, self.one_count)
