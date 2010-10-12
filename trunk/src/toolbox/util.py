import os, types, pylab
from toolbox.cartesian_product import cartesian_product
from pylab import svd, find, exp, log, pi, nan, mean, sqrt, array, dot

def read_simple_mapfile(filename, default_value=""):
    map = {}
    file = open(filename, 'r')
    for line in file.readlines():
        if (line.find('=') == -1):
            map[line.strip()] = default_value
        else:
            (key, value) = line.split('=')
            map[key.strip()] = value.strip()
    file.close()
    return map

def _mkdir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired " \
                      "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            _mkdir(head)
        if tail:
            os.mkdir(newdir)

def calc_rmse(vec1, vec2):
    """
        Calculates the RMSE (Root Mean Squared Error) between two vectors.
        Vectors can be given as lists.
    """
    return sqrt( mean( (array(vec1) - array(vec2))**2 ) )

def calc_r2(vec1, vec2):
    """
        Calculates the correlation coefficient (R^2) of two vectors.
        Vectors can be given as lists.
    """
    v1 = array(vec1)
    v2 = array(vec2)
    return dot(v1, v2.T)**2 / (dot(v1, v1.T) * dot(v2, v2.T))

def gcd(a,b=None):
    """ Return greatest common divisor using Euclid's Algorithm.
        a - can be either an integer or a list of integers
        b - if 'a' is an integer, 'b' should also be one. if 'a' is a list, 'b' should be None
    """
    if (b == None):
        if (a == []):
            return 1
        g = a[0]
        for i in range(1, len(a)):
            g = gcd(g, a[i])
        return g
    else:
        while b:      
          a, b = b, a % b
        return a

# choose function (number of way to choose k elements from a list of n)
def choose(n, k):
    """ 
        return the binomial coefficient of n over k
    """
    def rangeprod(k, n):
        """
            returns the product of all the integers in {k,k+1,...,n}
        """ 
        res = 1
        for t in range(k, n+1):
            res *= t
        return res
    
    if (n < k):
        return 0
    else:
        return (rangeprod(n-k+1, n) / rangeprod(1, k))

def median(v):
    if (len(v) == 0):
        return None
    sv = sorted(v)
    if (len(v) % 2 == 1):
        return (sv[(len(v)-1)/2])
    else:
        return (sv[len(v)/2 - 1] + sv[len(v)/2]) * 0.5

def subsets(items, minsize=0, maxsize=-1):
    def subsets_recursive(items, size, begin_index=0):
        """
            returns a list of all subsets of "items" of size == "size"
            e.g. subsets([1,2,3], 2) = [[1,2],[1,3],[2,3]]
        """
        if (items == []):
            return []
        elif (size == 0):
            return [[]]
        elif (size == 1):
            return [[x] for x in items[begin_index:]]
        else:
            s = []
            for i in range(begin_index, len(items)-1):
                x = items[i]
                for y in subsets_recursive(items, size-1, begin_index=i+1):
                    s.append([x] + y)
            return s
    
    if (maxsize == -1): # by default, return subsets of all sizes
        maxsize = len(items)
    s = []
    for size in range(minsize, maxsize+1):
        s += subsets_recursive(items, size)
    return s
    
def list2pairs(l):
    """
        Turns any list with N items into a list of (N-1) pairs of consecutive items.
    """
    res = []
    for i in range(len(l)-1):
        res.append((l[i], l[i+1]))
    return res

def sum(l):
    """
        Returns the sum of the items in the container class.
        This is more general than the build-in 'sum' function, because it is not specific for numbers.
        This function uses the '+' operator repeatedly on the items in the contrainer class.
        For example, if each item is a list, this will return the concatenation of all of them
    """
    return reduce(lambda x,y: x+y, l)

def flatten(l):
    """
        recursively turns any nested list into a regular list (using a DFS) 
    """
    res = []
    for x in l:
        if (isinstance(x, types.ListType)):
            res += flatten(x)
        else:
            res.append(x)
    return res

def rank(v):
    """
        Returns a list of the ranks from an unsorted list
    """
    sx = sorted([(v[i], i) for i in range(len(v))])
    rowidx = [i for (x,i) in sx]
    ranks = range(len(v))
    for i in range(len(v)):
        ranks[rowidx[i]] = i
    return ranks

def tiedrank(v):
    """
    Computes the ranks of the values in the vector x.
    If any x values are tied, tiedrank(x) computes their average rank.
    The return value is an adjustment for ties required by
    the nonparametric tests SIGNRANK and RANKSUM, and for the computation
    of Spearman's rank correlation.
    """

    sx = sorted([(v[i], i) for i in range(len(v))])
    rowidx = [i for (x,i) in sx]
    ranks = range(len(v))

    i = 0
    while (i < len(v)):
        j = 1
        while (i+j < len(v) and v[rowidx[i]] == v[rowidx[i+j]]):
            j += 1
        for k in range(i, i+j):
            ranks[rowidx[k]] = 1.0*i + 0.5*(j-1)
        i = i+j

    return ranks

def matrixrank(X):
    (U, M, V) = svd(X)
    return len(find(M > 1e-8))

def distribute(total, num_slots):
    if (num_slots == 1):
        return [[total]]
    if (total == 0):
        return [[0] * num_slots]
    all_options = []
    for i in range(total+1):
        for opt in distribute(total-i, num_slots-1):
            all_options.append([i] + opt)
    return all_options

def lsum(l):
    """
        returns a concatenations of all the members in 'l' assuming they are lists
    """
    s = []
    for member in l:
        if (type(member) == types.ListType):
            s += member
        elif (type(member) == types.TupleType):
            s += list(member)
        elif (type(member) == type(set())):
            s += list(member)
        else:
            s.append(member)
    return s

def log_sum_exp(v):
    if (len(v) == 0):
        raise ValueError("cannot run 'log_sum_exp' on an empty vector")
    elif (len(v) == 1):
        return v[0]
    else:
        max_v = max(v)
        s = 0
        for x in v:
            s += exp(x - max_v)
        return max_v + log(s)  

def log_subt_exp(x1, x2):
    """
        Assumes x1 > x2, otherwise throws an exception
    """
    if (x1 == x2):
        return nan
    elif (x1 > x2):
        return complex(x1 + log(1 - exp(x2-x1)), 0)
    else:
        return complex(x2 + log(1 - exp(x1-x2)), pi)
    
def multi_distribute(total_slots_pairs):
    multilist_of_options = []
    for (total, num_slots) in total_slots_pairs:
        multilist_of_options.append(distribute(total, num_slots))

    return [lsum(l) for l in cartesian_product(multilist_of_options)]

def plot_xy(cursor, query, prefix=None, color='b', marker='.', xlog=False, ylog=False, xlabel='', ylabel='', title=''):
    """
        Executes the 'query' which should return two numerical columns.
    """
    cursor.execute(query)
    x_list = []
    y_list = []
    mu_x = 0
    for row in cursor:
        (x, y) = row
        if (x != None and y != None):
            x_list.append(x)
            y_list.append(y)
    
    n = len(x_list)
    X = pylab.array(x_list)
    Y = pylab.array(y_list)
    pylab.figure()
    pylab.hold(True)
    pylab.plot(X, Y, color=color, marker=marker, linestyle='None')
    if (xlog):
        pylab.xscale('log')
    if (ylog):
        pylab.yscale('log')
    
    pylab.title(title + " (R^2 = %.2f)" % pylab.corrcoef(X,Y)[0,1]**2)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
    if (prefix != None):
        pylab.savefig('../res/%s.pdf' % prefix, format='pdf')
    pylab.hold(False)
    
###############################################################
def test():
    print tiedrank([5,4,3,2,1])
    print sum([[1,2,3,4,5],[1,2,3]])
    for s in subsets([(1,'a'),(2,'b'),(3,'c'),(4,'d'),(5,'e')], minsize=1, maxsize=2):
        print s
    
    print flatten([[1,2,3],[4,[5,6],[[7]]]])
    print lsum([[[1],[2]],3,set([4,5,6]),(7,8,9),10])
      
if (__name__ == '__main__'):
    test()
