import scipy as sp
import scipy.stats.stats as scipy_stats


def standardize(vector):
    mean = sp.nanmean(vector)
    standard_deviation = sp.nanstd(vector)
    return sp.divide(sp.subtract(vector, mean), standard_deviation)


def normalize(vector):
    minimum = sp.nanmin(vector)
    maximum = sp.nanmax(vector)
    return sp.divide(sp.subtract(vector, minimum), (maximum - minimum))


def pearson_r(p, q):
    indices = sp.logical_not(sp.logical_or(sp.isnan(p), sp.isnan(q)))
    return scipy_stats.pearsonr(p[indices], q[indices])[0]


def kendall_tau_b(p, q):
    indices = sp.logical_not(sp.logical_or(sp.isnan(p), sp.isnan(q)))
    return scipy_stats.kendalltau(p[indices], q[indices], method="asymptotic")[0]
