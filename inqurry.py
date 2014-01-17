# inqurry (infixed currying for integrated queries)

from operator import *
from itertools import *
from itertools import count as succ

id = lambda x:x

class inqurry:
    def __init__(self, hof, lof = None, **kwargs):
        self.hof = hof
        self.lof = lof if lof else id
        self.kwargs = kwargs

    def __ror__(self, xs):
        if self.kwargs:
            return self.hof(self.lof, xs, **self.kwargs)
        return self.hof(self.lof, xs)

    def __call__(self, lof = None, **kwargs):
        if lof:
            self.lof = lof
        if kwargs:
            self.kwargs = kwargs
        return self

    def __neg__(self):
        for k in self.kwargs:
            if type(self.kwargs[k]) is bool:
                self.kwargs[k] = not self.kwargs[k]
        return self

where    = inqurry(ifilter)
select   = inqurry(imap)
sort     = inqurry(lambda pred, xs, **kwargs:  sorted(xs, key = pred, **kwargs),
            reverse = False)
count    = inqurry(lambda pred, xs: sum(1 for x in xs if pred(x)))
take     = lambda n: inqurry(lambda pred, xs: islice(xs, 0, n))
group    = inqurry(lambda pred, xs: groupby(xs, pred))
order_by = lambda pred: pred
# then_by  =
# takewhile
# dropwhile

 # sort.__neg__ = negsort

# setattr(sort, '__neg__', negsort)

# --------------------------------------------------------------

from random import randint
from pprint import pprint

def complex_pts_test():
    # complex_pts = [complex(randint(0, 10), randint(0,10)) for _ in range(10)]
    complex_pts = [(2+5j), 6j, (5+7j), (4+9j), (3+0j), (4+9j), (10+4j), (1+1j), (3+4j), 8j]
    selected_pts = ( complex_pts |
            select (lambda _: int(_.real))       |
            where  (lambda _: _ > 2 and _ % 2)   |
            sort   (lambda _: _)                 )

    return selected_pts
    # print sorted(
    #     [r for r in [int(c.real) for c in complex_pts] if r > 2 and r % 2],
    #     reverse = True)

def words_test():
    words = ["zero", "one", "two", "three", "four", "five",
             "six", "seven", "eight", "nine", "ten"]

    selected_words =  ( words             |
                        order_by(len)     |
                        then_by()         |
                        take(5)           |
                        select(str.upper) )

def employee_test():
    employees = [dict(firstname='Joe', lastname='Bloggs', grade=3),
                 dict(firstname='Ola', lastname='Nordmann', grade=3),
                 dict(firstname='Kari', lastname='Nordmann', grade=2),
                 dict(firstname='Jane', lastname='Doe', grade=4),
                 dict(firstname='John', lastname='Doe', grade=3)]

    pprint (employees | sort(lambda _: _['grade'], reverse = True) )

if __name__ == '__main__':
    s_p = complex_pts_test()

    pprint( list( range(10) | sort ))
    pprint( list( range(10) | -sort ))


# group_iterators = words | sort(len) | group(len)

# x = chain(*map(lambda _: sorted(_[1]), group_iterators))

# print list( x | take(5) | select(str.upper) )

