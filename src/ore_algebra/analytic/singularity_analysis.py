# coding: utf-8 - vim: tw=80
r"""
Bounds on sequences by singularity analysis

Main author: Ruiwen Dong <ruiwen.dong@polytechique.edu>

This module currently requires Sage development branch u/mmezzarobba/tmp/bterms
(= Sage 9.5.beta0 + #32229 + #32451 + a patch for combining BTerms with the same
growth); ``check_seq_bound`` and the tests depending on it may need additional
patches.

EXAMPLES::

    sage: from ore_algebra import (OreAlgebra, DFiniteFunctionRing,
    ....:         UnivariateDFiniteFunction)
    sage: from ore_algebra.analytic.singularity_analysis import (
    ....:         bound_coefficients, check_seq_bound)

    sage: Pols_z.<z> = PolynomialRing(QQ)
    sage: Diff.<Dz> = OreAlgebra(Pols_z)

Membrane example::

    sage: seqini = [72, 1932, 31248, 790101/2, 17208645/4, 338898609/8, 1551478257/4]
    sage: deq = (8388593*z^2*(3*z^4 - 164*z^3 + 370*z^2 - 164*z + 3)*(z + 1)^2*(z^2 - 6*z + 1)^2*(z - 1)^3*Dz^3
    ....: + 8388593*z*(z + 1)*(z^2 - 6*z + 1)*(66*z^8 - 3943*z^7 + 18981*z^6 - 16759*z^5 - 30383*z^4 + 47123*z^3 - 17577*z^2 + 971*z - 15)*(z - 1)^2*Dz^2
    ....: + 16777186*(z - 1)*(210*z^12 - 13761*z^11 + 101088*z^10 - 178437*z^9 - 248334*z^8 + 930590*z^7 - 446064*z^6 - 694834*z^5 + 794998*z^4 - 267421*z^3 + 24144*z^2 - 649*z + 6)*Dz
    ....: + 6341776308*z^12 - 427012938072*z^11 + 2435594423178*z^10 - 2400915979716*z^9 - 10724094731502*z^8 + 26272536406048*z^7 - 8496738740956*z^6 - 30570113263064*z^5 + 39394376229112*z^4 - 19173572139496*z^3 + 3825886272626*z^2 - 170758199108*z + 2701126946)

    sage: asy = bound_coefficients(deq, seqini, order=5, prec=200) # long time (5 s)
    doctest:...: FutureWarning: This class/method/function is marked as
    experimental. ...
    sage: asy # long time
    1.000...*5.828427124746190?^n*(([8.0719562915...] + [+/- ...]*I)*n^3*log(n)
    + ([1.3714048996...82527...] + [+/- ...]*I)*n^3
    + ([50.509130873...07157...] + [+/- ...]*I)*n^2*log(n)
    + ([29.698551451...84781...] + [+/- ...]*I)*n^2
    + ...
    + ([-0.283779713...91869...] + [+/- ...]*I)*n^(-1)*log(n)
    + ([35.493938347...65227...] + [+/- ...]*I)*n^(-1)
    + B([115882.8...]*n^(-2)*log(n)^2, n >= 50))

    sage: DFR = DFiniteFunctionRing(deq.parent())
    sage: ref = UnivariateDFiniteFunction(DFR, deq, seqini)
    sage: check_seq_bound(asy.expand(), ref, list(range(100)) + list(range(200, 230)) + [1000]) # long time

Algebraic example::

    sage: deq = (4*z^4 - 4*z^3 + z^2 - 2*z + 1)*Dz + (-4*z^3 + 4*z^2 - z - 1)
    sage: bound_coefficients(deq, [1], order=5) # long time (13 s)
    1.000...*2^n*([0.564189583547...]*n^(-1/2) + [-0.105785546915...]*n^(-3/2)
    + [-0.117906807499...]*n^(-5/2) + [-0.375001499318...]*n^(-7/2)
    + [-1.255580304110...]*n^(-9/2) + B([1304.15...]*n^(-11/2), n >= 50))

Diagonal example (Sage is not yet able to correctly combine and order the error
terms here)::

    sage: seqini = [1, -3, 9, -3, -279, 2997]
    sage: deq = (z^2*(81*z^2 + 14*z + 1)*Dz^3 + 3*z*(162*z^2 + 21*z + 1)*Dz^2
    ....:        + (21*z + 1)*(27*z + 1)*Dz + 3*(27*z + 1))

    sage: bound_coefficients(deq, seqini, order=2) # long time (3.5 s)
    1.000000000000000*9.00000000000000?^n*(([0.30660...] + [0.14643...]*I)*(e^(I*arg(-0.77777...? + 0.62853...?*I)))^n*n^(-3/2)
    + ([-0.26554...] + [-0.03529...]*I)*(e^(I*arg(-0.77777...? + 0.62853...?*I)))^n*n^(-5/2)
    + B([16.04...]*(e^(I*arg(-0.77777...? + 0.62853...?*I)))^n*n^(-7/2), n >= 50)
    + ([0.30660...] + [-0.14643...]*I)*(e^(I*arg(-0.77777...? - 0.62853...?*I)))^n*n^(-3/2)
    + ([-0.26554...] + [0.03529...]*I)*(e^(I*arg(-0.77777...? - 0.62853...?*I)))^n*n^(-5/2)
    + B([16.04...]*(e^(I*arg(-0.77777...? - 0.62853...?*I)))^n*n^(-7/2), n >= 50)
    + B([2.06...]*n^(-7/2), n >= 50))

Complex exponents example::

    sage: deq = (z-2)^2*Dz^2 + z*(z-2)*Dz + 1
    sage: seqini = [1, 2, -1/8]
    sage: asy = bound_coefficients(deq, seqini, order=3) # long time (2 s)
    sage: asy # long time
    1.000000000000000*(1/2)^n*(([1.124337...] + [0.462219...]*I)*n^(-0.500000...? + 0.866025...?*I)
    + ([1.124337...] + [-0.462219...]*I)*n^(-0.500000...? - 0.866025...?*I)
    + ([-0.400293...] + [0.973704...]*I)*n^(-1.500000...? + 0.866025...?*I)
    + ([-0.400293...] + [-0.973704...]*I)*n^(-1.500000...? - 0.866025...?*I)
    + ([0.451623...] + [-0.356367...]*I)*n^(-2.500000...? + 0.866025...?*I)
    + ([0.451623...] + [0.356367...]*I)*n^(-2.500000...? - 0.866025...?*I)
    + B([2761.73...]*n^(-7/2), n >= 50))

    sage: ref = UnivariateDFiniteFunction(DFR, deq, seqini)
    sage: #check_seq_bound(asy.expand(), ref, range(1000)) # buggy
    sage: # Temporary workaround
    sage: from ore_algebra.analytic.singularity_analysis import contribution_all_singularity, eval_bound
    sage: b = contribution_all_singularity(seqini, deq, total_order=3) # long time (1.9 s)
    sage: all(eval_bound(b[1], j).contains_exact(ref[j]) for j in range(b[0], 150)) # long time
    True


"""

import logging
import time

from sage.all import *

from sage.categories.cartesian_product import cartesian_product
from sage.rings.asymptotic.asymptotic_ring import AsymptoticRing
from sage.rings.asymptotic.growth_group import (
        ExponentialGrowthGroup,
        GrowthGroup,
        MonomialGrowthGroup,
)
try:
    from sage.rings.asymptotic.term_monoid import BTermMonoid
except ImportError:
    raise ImportError("the singularity_analysis module requires SageMath "
            "version 9.5 or later") # XXX
from sage.rings.asymptotic.term_monoid import (
        BTerm,
        BTermMonoid,
        ExactTermMonoid,
)
from sage.rings.asymptotic.term_monoid import DefaultTermMonoidFactory
from sage.symbolic.operators import add_vararg

from ..ore_algebra import OreAlgebra
from . import utilities
from .bounds import DiffOpBound
from .differential_operator import DifferentialOperator
from .local_solutions import (
        critical_monomials,
        FundamentalSolution,
        LocalBasisMapper,
        log_series,
        LogSeriesInitialValues,
)
from .path import Point
from .ui import multi_eval_diffeq

logger = logging.getLogger(__name__)

def truncate_tail(f, deg, min_n, w, kappa = None, logn = None):
    """
    Truncate and bound an expression f(1/n) to a given degree

    If kappa is None, 1/n^(deg+t) (t > 0) will be truncated to
        1/n^deg * CB(0).add_error(1/min_n^t)
    If kappa is not None, then 1/n^(deg+t) will be truncated to
        logn^kappa/n^deg * CB(0).add_error(**)

    INPUT:

    - f : polynomial in w = 1/n to be truncated
    - deg : desired degree (in w) of polynomial after truncation
    - min_n : positive number where n >= min_n is guaranteed
    - w : element of polynomial ring, representing 1/n
    - kappa : integer, desired degree (in logn) of polynomial after truncation
    - logn : element of polynomial ring, representing log(n)

    OUTPUT:

    - g : a polynomial in CB[w] such that f is in its range when n >= min_n
    """
    R = f.parent()
    CB = R.base_ring()
    g = R(0)
    if kappa is None:
        for c, mon in f:
            deg_w = mon.degree(w)
            if deg_w > deg:
                tuple_mon_g = tuple(map(lambda x, y: x - y, mon.exponents()[0],
                                        (w**(deg_w - deg)).exponents()[0]))
                mon_g = prod(R.gens()[j]**(tuple_mon_g[j])
                             for j in range(len(tuple_mon_g)))
                c_g = ((c if c.mid() == 0 else CB(0).add_error(c.above_abs()))
                        / CB(min_n**(deg_w - deg)))
                g = g + c_g * mon_g
            else:
                g = g + c*mon
    else:
        for c, mon in f:
            deg_w = mon.degree(w)
            deg_logn = mon.degree(logn)
            if deg_w >= deg:
                tuple_mon_g = tuple(map(lambda x, y, z: x - y + z, mon.exponents()[0],
                                        (w**(deg_w - deg)).exponents()[0],
                                        (logn**(kappa - deg_logn)).exponents()[0]))
                mon_g = prod(R.gens()[j]**(tuple_mon_g[j])
                             for j in range(len(tuple_mon_g)))
                c_g = ((c if c.mid() == 0 else CB(0).add_error(c.above_abs()))
                        / CB(min_n**(deg_w - deg))) * CB(min_n).log().pow(deg_logn - kappa)
                g = g + c_g * mon_g
            else:
                g = g + c*mon
    return g

def truncate_tail_SR(val, f, deg, min_n, w, kappa, logn, n):
    """
    Truncate and bound an expression n^val*f(1/n) to a given degree
    1/n^(deg+t), t>=0 will be truncated to
        logn^kappa/n^deg * CB(0).add_error(**)

    INPUT:

    - f : polynomial in w = 1/n to be truncated
    - deg : desired degree (in n) of expression after truncation
    - min_n : positive number where n >= min_n is guaranteed
    - w : element of polynomial ring, representing 1/n
    - kappa : integer, desired degree (in logn) of polynomial after truncation
    - logn : element of polynomial ring, representing log(n)
    - n : symbolic ring variable

    OUTPUT:

    - g : an Symbolic Ring expression in variable n, such that f is in its range when n >= min_n
    """
    R = f.parent()
    CB = R.base_ring()
    g = SR(0)
    for c, mon in f:
        deg_w = mon.degree(w)
        deg_logn = mon.degree(logn)
        if val.real() - deg_w <= deg:
            c_g = ((c if c.mid() == 0 else CB(0).add_error(c.above_abs()))
                    / CB(min_n).pow(deg + deg_w - val.real())) * CB(min_n).log().pow(deg_logn - kappa)
            g = g + c_g * n**deg * log(n)**kappa
        else:
            g = g + c * n**(val - deg_w) * log(n)**deg_logn
    return g

################################################################################
# Contribution of a logarithmic monomial
# (variant with error bounds of Sage's SingularityAnalysis)
#################################################################################

def Lie_der(f, tup_x_k):
    """
    find f'

    INPUT:

    - f : polynomial in variables x_0, x_1, ..., x_(n-1)
    - tup_x_k : tuple of variables x_0, x_1, ..., x_n

    OUTPUT:

    - f_prime : f', where (x_i)' = x_(i+1)
    """
    n = len(tup_x_k) - 1
    f_prime = sum([derivative(f, tup_x_k[k]) * tup_x_k[k+1] for k in range(n)])
    return f_prime

def _der_expf_R(k, R):
    """
    Auxiliary function used in recursion for der_expf

    Find an expression for [(d/dx)^k exp(f(x))]/exp(f(x)) given in a polynomial
    ring R
    """
    tup_f_k = R.gens()
    if k == 0:
        return R(1)
    else:
        der_k_minus_one = _der_expf_R(k-1, R)
        der_k = tup_f_k[0] * der_k_minus_one + Lie_der(der_k_minus_one, tup_f_k)
        return der_k

def der_expf(k):
    """
    Find an expression for [(d/dx)^k exp(f(x))]/exp(f(x))
    """
    R = PolynomialRing(ZZ, 'f', k)
    der_k = _der_expf_R(k, R)
    return der_k

def truncated_psi(n, m, v, logz):
    """
    Compute psi^(m)(z) truncated at z^(-m-2n-1) with error bound of order
    z^(-m-2n-2)

    INPUT:

    - n : integer, non-negative
    - m : integer, non-negative
    - v : element of polynomial ring, representing 1/z
    - logz : element of polynomial ring, representing log(z)
    """
    R = v.parent()
    CB = R.base_ring()
    Enz_coeff = (2*abs(bernoulli(2*n+2)) * (m + 2*n + 2)**(m + 2*n + 2)
            / (2*n + 1)**(2*n + 1) / (m + 1)**(m + 1)
            * gamma(m+2) / (2*n + 1) / (2*n + 2))
    if m == 0:
        return R(logz - v / 2
                - sum(bernoulli(2*k)*v**(2*k)/(2*k) for k in range(1,n+1))
                + CB(0).add_error(Enz_coeff)*v**(2*n+2))
    else:
        return R((-1)**(m+1) * (gamma(m) * v**m + gamma(m+1) * v**(m+1) / 2
            + sum(bernoulli(2*k)*v**(2*k+m)*rising_factorial(2*k+1, m-1)
                  for k in range(1,n+1)))
            + CB(0).add_error(Enz_coeff)*v**(2*n+m+2))

def truncated_logder(alpha, l, order, v, logz, min_n=None):
    """
    Find a truncated expression with error bound for
    [(d/dα)^l (Γ(n+α)/Γ(α))] / (Γ(n+α)/Γ(α))

    INPUT:

    - alpha : complex number α, !!cannot be negative integer or zero!!
    - l : integer, non-negative
    - order : order of truncation
    - v : element of polynomial ring, representing 1/(n+α)
    - logz : element of polynomial ring, representing log(n+α)
    - min_n : positive number where n >= min_n is guaranteed, min_n > -alpha
      needed

    OUTPUT:

    a polynomial in CB[v] such that [(d/dα)^l (Γ(n+α)/Γ(α))] / (Γ(n+α)/Γ(α)) is
    in its range when n >= max(s*|alpha|, min_n)
    """
    list_f = []
    R = v.parent()
    CB = R.base_ring()
    for m in range(l):
        n = max(0, ceil((order - m - 1)/2))
        Enz_coeff = (abs(bernoulli(2*n+2)) * (m + 2*n + 2)**(m + 2*n + 2)
                / (2*n + 1)**(2*n + 1) / (m + 1)**(m + 1)
                * gamma(m+2) / (2*n + 1) / (2*n + 2))
        list_f.append(truncated_psi(n, m, v, logz) - CB(alpha).psi(m))
        if not min_n is None:
            list_f[-1] = truncate_tail(list_f[-1], order+1, min_n + alpha, v)
    p = der_expf(l)
    if not min_n is None:
        return R(1) if l == 0 else truncate_tail(p(list_f), order+1, min_n + alpha, v)
    else:
        return p(list_f)

def truncated_ratio_gamma(alpha, order, u, s):
    """
    Find a truncated expression with error bound for Γ(n+α)/Γ(n+1)/(n+α/2)^(α-1)

    INPUT:

    - alpha : complex number α, !!cannot be negative integer or zero!!
    - order : order of truncation
    - u : element of polynomial ring, representing 1/(n+α/2)
    - s : positive number where n >= s*|alpha| is guaranteed, s > 2

    OUTPUT:

    - ratio_gamma : a polynomial in CB[u] such that Γ(n+α)/Γ(n+1)/(n+α/2)^(α-1)
      is in its range when n >= s*|alpha|
    """
    CB = u.parent().base_ring()
    rho = CB(alpha/2)
    n_gam = ceil((1+order)/2)
    #Compute B_2l^2r(r) where B_n^m(r) is the generalized Bernoulli polynomial
    t = polygen(CB, 't')
    foo = (t._exp_series(2*n_gam + 1) >> 1)
    foo = -2*rho*foo._log_series(2*n_gam)
    foo = (foo >> 2) << 2
    foo = foo._exp_series(2*n_gam)
    series_gen_bern = [c*ZZ(n).factorial() for n, c in enumerate(foo)]

    #Compute B_2l^2r(|r|) where B_n^m(|r|) is the generalized Bernoulli polynomial
    foo = (t._exp_series(2*n_gam + 2) >> 1)
    foo = -2*abs(rho)*foo._log_series(2*n_gam+1)
    foo = (foo >> 2) << 2
    foo = foo._exp_series(2*n_gam+1)
    series_gen_bern_abs = [c*ZZ(n).factorial() for n, c in enumerate(foo)]

    ratio_gamma_asy = sum(
            CB((1 - 2*rho).rising_factorial(2*j) / factorial(2*j)
                * series_gen_bern[2*j]) * u**(2*j)
            for j in range(n_gam))
    Rnw_bound = ((1 - 2*rho.real()).rising_factorial(2*n_gam) / factorial(2*n_gam)
            * CB(abs(series_gen_bern_abs[2*n_gam]))
            * CB(abs(alpha.imag())/2/s).exp()
            * CB((s+1/2)/(s-1/2)).pow(max(0, -2*rho.real()+1+2*n_gam)))
    ratio_gamma = ratio_gamma_asy + CB(0).add_error(Rnw_bound) * u**(2*n_gam)
    return ratio_gamma

def truncated_power(alpha, order, w, s):
    """
    Compute a bound for a truncated (1 + α/2n)^(α-1)

    INPUT:

    - alpha : complex number α, !!cannot be negative integer or zero!!
    - order : order of truncation
    - w : element of polynomial ring, representing 1/n
    - s : positive number where n >= s*|alpha| is guaranteed, s > 2

    OUTPUT:

    - trunc_power : a polynomial in CB[w] such that (1 + α/2n)^(α-1) is in its
      range when n >= s*|alpha|
    """
    CB = w.parent().base_ring()
    alpha_CB = CB(alpha)
    Mr = (CB(abs(alpha)).pow(order+1) / (1 - 1/s)
            * CB(abs(alpha.imag())/2).exp()
            * (CB(3/2).pow(alpha.real() - 1) if alpha.real() - 1 > 0
               else CB(1/2).pow(alpha.real() - 1)))
    t = polygen(CB, 't')
    foo = (alpha_CB - 1) * (1 + alpha_CB/2 * t)._log_series(order + 1)
    foo = foo._exp_series(order + 1)
    trunc_power = foo(w) + CB(0).add_error(Mr) * w**(order+1)
    return trunc_power

def bound_coeff_mono(alpha, l, deg, w, logn, s=5, min_n=50):
    """
    Compute a bound for [z^n] (1-z)^(-α) * log(1/(1-z))^l,
    of the form n^(α-1) * P(1/n, log(n))

    INPUT:

    - alpha : complex number, representing α
    - l : non-negative integer
    - deg : degree of P wrt. the variable 1/n
    - w : variable representing 1/n
    - logn : element of the same polynomial ring as w, variable representing
      log(n)
    - s : positive number where n >= s*|alpha| is guaranteed, s > 2
    - min_n : positive number where n >= min_n is guaranteed, min_n > -alpha
      needed

    OUTPUT:

    - P : polynomial in w, logn
    """
    R = w.parent()
    CB = R.base_ring()
    v, logz, u, _, _ = R.gens()
    order = max(0, deg - 1)
    if not (QQbar(alpha).is_integer() and QQbar(alpha) <= 0):
        # Value of 1/Γ(α)
        c = CB(1/gamma(alpha))
        # Bound for (n+α/2)^(1-α) * Γ(n+α)/Γ(n+1) [Dong2021, Prop 4.5]
        f = truncated_ratio_gamma(alpha, order, u, s)
        bound_error_u = CB(abs(alpha/2)**order / (1 - 1/(2*s)))
        truncated_u = (sum(CB(-alpha/2)**(j-1) * w**j for j in range(1, order+1))
                + CB(0).add_error(bound_error_u) * w**(order+1))
        f_z = truncate_tail(f.subs({u : truncated_u}), deg, min_n, w)
        # Bound for F = [(d/dα)^l (Γ(n+α)/Γ(α)Γ(n+1))] / (Γ(n+α)/Γ(α)Γ(n+1))
        # [Dong2021, p. 17]
        g = truncated_logder(alpha, l, order, v, logz, min_n)
        bound_error_v = CB(abs(alpha)**order / (1 - 1/s))
        truncated_v = (sum(CB(-alpha)**(j-1) * w**j for j in range(1, order+1))
                + CB(0).add_error(bound_error_v) * w**(order+1))
        bound_error_logz = (CB(log(2)+1/2)
                * CB(2*abs(alpha)).pow(order+1)
                / CB(1 - 2/s))
        truncated_logz = (logn
                - sum(CB(-alpha)**j * w**j / j
                      for j in range(1, order+1))
                + CB(0).add_error(bound_error_logz) * w**(order+1))
        g_z = truncate_tail(
                g.subs({v : truncated_v, logz : truncated_logz}),
                deg, min_n, w)
        # Bound for (1 + α/2n)^(α-1) = (n+α/2)^(α-1) * n^(1-α) [Dong2021, p. 16]
        h_z = truncated_power(alpha, order, w, s)
        product_all = c * f_z * g_z * h_z
        return truncate_tail(product_all, deg, min_n, w)
    elif l == 0:
        # Terminating expansion of the form (1-z)^N, N = -α ∈ ℕ
        if min_n <= -int(alpha):
            # XXX increase min_n or compute the terms of deg min_n..n instead
            raise ValueError("min_n too small!")
        return R(0)
    else:
        # |alpha| decreases, so n >= s*|alpha| still holds
        poly_rec_1 = bound_coeff_mono(alpha + 1, l, deg, u, logz, s, min_n - 1)
        poly_rec_2 = bound_coeff_mono(alpha + 1, l - 1, deg, u, logz, s, min_n - 1)
        #u = 1/(n-1)
        bound_error_u = CB(1 / (1 - 1/(min_n - 1)))
        truncated_u = (sum(CB(1) * w**j for j in range(1, order+1))
                + CB(0).add_error(bound_error_u) * w**(order+1))
        bound_error_logz = CB(abs(log(2) * 2**(order+1)) / (1 - 2/(min_n - 1)))
        truncated_logz = (logn
                - sum(CB(1) * w**j / j
                      for j in range(1, order+1))
                + CB(0).add_error(bound_error_logz) * w**(order+1))
        ss = (CB(alpha) * poly_rec_1.subs({u : truncated_u, logz : truncated_logz})
            + CB(l) * poly_rec_2.subs({u : truncated_u, logz : truncated_logz}))
        return truncate_tail(ss, deg, min_n, w)

#################################################################################
# Contribution of a single regular singularity
#################################################################################

def _modZ_class_ini(dop, inivec, leftmost, mults, struct):
    r"""
    Compute a LogSeriesInitialValues object corresponding to the part with a
    given local exponent mod 1 of a local solution specified by a vector of
    initial conditions.
    """
    values = { (sol.shift, sol.log_power): c
                for sol, c in zip(struct, inivec)
                if sol.leftmost == leftmost }
    ini = LogSeriesInitialValues(dop=dop, expo=leftmost, values=values,
            mults=mults, check=False)
    return ini

def _my_log_series(dop, bwrec, inivec, leftmost, mults, struct, order):
    r"""
    Similar to _modZ_class_ini() followed by log_series(), but attempts to
    minimize interval swell by unrolling the recurrence in exact arithmetic
    (once per relevant initial value) and taking a linear combination.

    The output is a list of lists, not vectors.
    """
    log_len = sum(m for _, m in mults)
    res = [[inivec.base_ring().zero()]*log_len for _ in range(order)]
    for sol, c in zip(struct, inivec):
        if c.is_zero() or sol.leftmost != leftmost:
            continue
        values = { (sol1.shift, sol1.log_power): QQ.zero()
                   for sol1 in struct if sol1.leftmost == leftmost }
        values[sol.shift, sol.log_power] = QQ.one()
        ini = LogSeriesInitialValues(dop=dop, expo=leftmost, values=values,
                mults=mults, check=False)
        ser = log_series(ini, bwrec, order)
        for i in range(order):
            for j, a in enumerate(ser[i]):
                res[i][j] += c*a
    return res

class SingularityAnalyzer(LocalBasisMapper):

    def __init__(self, dop, inivec, *, rho, rad, Expr, abs_order, min_n,
                 coord_big_circle, struct):

        super().__init__(dop)

        self.inivec = inivec
        self.rho = rho
        self.rad = rad
        self.Expr = Expr
        self.abs_order = abs_order
        self.min_n = min_n
        self.coord_big_circle = coord_big_circle
        self._local_basis_structure = struct

    def process_modZ_class(self):

        order = (self.abs_order - self.leftmost.real()).ceil()
        # XXX don't hardocode this; ensure order1 ≥ bwrec.order
        order1 = order + 49
        # XXX Works, and should be faster, but leads to worse bounds due to
        # using the recursion in interval arithmetic
        # ini = _modZ_class_ini(self.edop, self.inivec, self.leftmost, self.shifts,
        #                       self._local_basis_structure) # TBI?
        # ser = log_series(ini, self.shifted_bwrec, order1)
        ser = _my_log_series(self.edop, self.shifted_bwrec, self.inivec,
                self.leftmost, self.shifts, self._local_basis_structure, order1)

        CB = CBF # XXX
        smallrad = self.rad - CB(self.rho).below_abs()
        # XXX do we really a bound on the tail *of order `order`*? why not
        # compute a bound on the tail of order `order1` and put everything else
        # in the "explicit terms" below?
        vb = _bound_tail(self.edop, self.leftmost, smallrad, order, ser)

        # XXX why an integer?
        s = floor(self.min_n / (abs(self.leftmost) + abs(order)))
        if s <= 2: # XXX take s=3 instead (cf. def. of N0), maybe update n0
            raise ValueError("min_n too small! Cannot guarantee s>2")

        # (Bound on) Maximum power of log that may occur the sol defined by ini.
        # (We could use the complete family of critical monomials for a tighter
        # bound when order1 < max shift, since for now we currently are
        # computing it anyway...)
        assert self.shifts[0][0] == 0 and order1 > 0
        kappa = max(k for shift, mult in self.shifts if shift < order1
                      for k, c in enumerate(ser[shift]) if not c.is_zero())
        kappa += sum(mult for shift, mult in self.shifts if shift >= order1)

        bound_lead_terms, dom_big_circle = _bound_local_integral_explicit_terms(
                self.rho, self.leftmost, order, self.Expr, s, self.min_n, ser[:order],
                self.coord_big_circle)
        bound_int_SnLn = _bound_local_integral_of_tail(self.rho,
                self.leftmost, order, self.Expr, s, self.min_n, vb, kappa)

        logger.debug("sing=%s, valuation=%s", self.rho, self.leftmost)
        logger.debug("  leading terms = %s", bound_lead_terms)
        logger.debug("  tail bound = %s", bound_int_SnLn)

        data = [kappa, bound_lead_terms + bound_int_SnLn, dom_big_circle]

        # XXX abusing FundamentalSolution somewhat; not sure if log_power=kappa
        # is really appropriate; consider creating another type of record
        # compatible with FundamentalSolution if this stays
        sol = FundamentalSolution(leftmost=self.leftmost, shift=ZZ.zero(),
                                  log_power=kappa, value=data)
        self.irred_factor_cols.append(sol)

def _bound_tail(dop, leftmost, smallrad, order, series):
    r"""
    Upper-bound the tail of order ``order`` of a logarithmic series solution of
    ``dop`` with exponents in ``leftmost`` + ℤ, on a disk of radius
    ``smallrad``, using ``order1`` ≥ ``order`` explicitly computed terms given
    as input in ``series`` and a bound based on the method of majorants for the
    terms of index ≥ ``order1``.
    """
    assert order <= len(series)
    maj = DiffOpBound(dop, leftmost=leftmost, pol_part_len=30, # XXX
                                                    bound_inverse="solve")
    ordrec = maj.dop.degree()
    last = list(reversed(series[-ordrec:]))
    order1 = len(series)
    # Coefficients of the normalized residual in the sense of [Mez19, Sec.
    # 6.3], with the indexing conventions of [Mez19, Prop. 6.10]
    CB = CBF # TBI
    res = maj.normalized_residual(order1, last, Ring=CB)
    # Majorant series of [the components of] the tail of the local expansion
    # of f at ρ. See [Mez19, Sec. 4.3] and [Mez19, Algo. 6.11].
    tmaj = maj.tail_majorant(order1, [res])
    # Make a second copy of the bound before we modify it in place.
    tmaj1 = maj.tail_majorant(order1, [res])
    # Shift it (= factor out z^order) ==> majorant series of the tails
    # of the coefficients of log(z)^k/k!
    tmaj1 >>= -order
    # Bound on the *values* for |z| <= smallrad of the analytic functions
    # appearing as coefficients of log(z)^k/k! in the tail of order 'order1' of
    # the local expansion
    tb = tmaj1.bound(smallrad)
    # Bound on the intermediate terms
    ib = sum(smallrad**n1 * max(c.above_abs() for c in vec)
            for n1, vec in enumerate(series[order:]))
    # Same as tb, but for the tail of order 'order'
    return tb + ib

def _bound_local_integral_of_tail(rho, val_rho, order, Expr, s, min_n, vb, kappa):

    _, _, _, w, logn = Expr.gens()

    CB = CBF # These are error terms, no need for high prec. Still, TBI.
    RB = RBF

    # Change representation from log(z-ρ) to log(1/(1 - z/ρ))
    # The h_i are cofactors of powers of log(z-ρ), not log(1/(1-z/ρ)).
    # Define the B polynomial in a way that accounts for that.
    ll = abs(CB(-rho).log())
    B = vb*RB['z']([
            sum([ll**(m - j) * binomial(m, j) / factorial(m)
                    for m in range(j, kappa + 1)])
            for j in range(kappa + 1)])

    # Sub polynomial factor for bound on S(n)
    cst_S = CB(0).add_error(CB(abs(rho)).pow(val_rho.real()+order)
            * ((abs(CB(rho).arg()) + 2*RB(pi))*abs(val_rho.imag())).exp()
            * CB(1 - 1/min_n).pow(CB(-min_n-1)))
    bound_S = cst_S*B(CB(pi)+logn)
    # Sub polynomial factor for bound on L(n)
    if val_rho + order <= 0:
        C_nur = 1
    else:
        C_nur = 2 * (CB(e) / (CB(val_rho.real()) + order)
                            * (s - 2)/(2*s)).pow((RB(val_rho.real()) + order))
    cst_L = (CB(0).add_error(C_nur * CB(1/pi)
                                * CB(abs(rho)).pow(RB(val_rho.real())+order))
        * ((abs(CB(rho).arg()) + 2*RB(pi))*abs(val_rho.imag())).exp())
    bound_L = cst_L*B(CB(pi)+logn)

    return (bound_S + bound_L) * w**order

def _bound_local_integral_explicit_terms(rho, val_rho, order, Expr, s, min_n, ser,
        coord_big_circle):

    _, _, _, w, logn = Expr.gens()
    CB = Expr.base_ring()

    # Rewrite the local expansion in terms of new variables Z = z - ρ,
    # L = log(1/(1-z/rho))

    Z, L = PolynomialRing(CB, ['Z', 'L']).gens()
    mylog = CB.coerce(-rho).log() - L # = log(z - ρ) for Im(z) ≥ 0
    locf_ini_terms = sum(c/ZZ(k).factorial() * mylog**k * Z**shift
                         for shift, vec in enumerate(ser)
                         for k, c in enumerate(vec))

    bound_lead_terms = sum(
            c * CB(- rho).pow(CB(val_rho+degZ))
              * w**(degZ)
              * bound_coeff_mono(-val_rho-degZ, degL, order - degZ,
                                  w, logn, s, min_n)
            for ((degZ, degL), c) in locf_ini_terms.iterator_exp_coeff())

    # Values of the tail of the local expansion.
    # With the first square (and possibly some others), the argument of the
    # log that we substitute for L crosses the branch cut. This is okay
    # because the enclosure returned by Arb takes both branches into
    # account.

    # XXX why do we do this here? to access locf_ini_terms, presumably--but
    # this means we have to pass coord_big_circle, so the gain is not clear
    _zeta = CB(rho)
    dom_big_circle = [
            (_z-_zeta).pow(CB(val_rho))
                * locf_ini_terms(_z-_zeta, (~(1-_z/_zeta)).log())
            for _z in coord_big_circle]

    return bound_lead_terms, dom_big_circle

def contribution_single_singularity(deq, ini, rho, rad,
        coord_big_circle, rel_order, min_n, prec_bit):

    z = deq.parent().base_ring().gens()[0]
    rad = RBF(rad)

    eps = RBF.one() >> prec_bit + 13
    tmat = deq.numerical_transition_matrix([0, rho], eps, assume_analytic=True)
    coord_all = tmat*ini

    ldop = DifferentialOperator(deq).shift(Point(rho, deq))

    # Redundant work; TBI
    # (Cases where we really need this to detect non-analyticity are rare...)
    crit = critical_monomials(ldop)

    # XXX could move to SingularityAnalyzer if we no longer return min_val_rho
    nonanalytic = [sol for sol in crit if not (
        sol.leftmost.is_integer()
        and sol.leftmost + sol.shift >= 0
        and all(c.is_zero() for term in sol.value.values() for c in term[1:]))]
    if not nonanalytic:
        return
    min_val_rho = (nonanalytic[0].leftmost + nonanalytic[0].shift).real()
    abs_order = rel_order + min_val_rho

    # XXX split in v, logz and u, w, logn?
    Expr = PolynomialRing(ComplexBallField(prec_bit), ['v', 'logz', 'u', 'w', 'logn'], order='lex')

    analyzer = SingularityAnalyzer(dop=ldop, inivec=coord_all, rho=rho,
            rad=rad, Expr=Expr, abs_order=abs_order, min_n=min_n,
            coord_big_circle=coord_big_circle, struct=crit)
    data = analyzer.run()

    list_val_rho = [sol.leftmost for sol in data]
    list_bound = [sol.value[1] for sol in data]
    val_big_circle = [sum(sol.value[2][j] for sol in data)
                      for j in range(len(coord_big_circle))]
    max_kappa = max(sol.value[0] for sol in data)

    return list_val_rho, list_bound, val_big_circle, max_kappa, min_val_rho

################################################################################
# Exponentially small error term
################################################################################

def numerical_sol_big_circle(deq, ini, dominant_sing, rad, halfside, prec_bit):
    """
    Compute numerical solutions of f on big circle of radius rad

    INPUT:

    - ini : vector, coefficients corresponding to the basis at zero
    - deq : a linear ODE that the generating function satisfies
    - dominant_sing : list of algebraic numbers, list of dominant singularities
    - rad : radius of big circle
    - halfside : half of side length of covering squares
    - prec_bit : integer, approximated desired bit precision
    """
    logger.info("Bounding on large circle...")
    clock = utilities.Clock()
    clock.tic()

    I = CBF.gen(0)
    eps = RBF.one() >> 100
    rad = RBF(rad) # XXX temporary
    halfside = RBF(halfside)

    sings = [CBF(s) for s in dominant_sing]
    sings.sort(key=lambda s: s.arg())
    num_sings = len(sings)
    pairs = []
    num_sq = 0
    for j0 in range(num_sings):
        j1 = (j0 + 1) % num_sings
        arg0 = sings[j0].arg()
        arg1 = sings[j1].arg()
        if j1 == 0:
            # last arc is a bit special: we need to add 2*pi to ending
            arg1 += 2*RBF.pi()

        hub = rad * ((arg0 + arg1)/2 * I).exp()
        halfarc = (arg1 - arg0)/2
        np = ZZ(((halfarc*rad / (2*halfside)).above_abs()).ceil()) + 2
        num_sq += np
        circle_upper = [(hub*(halfarc*k/np*I).exp()).add_error(halfside)
                        for k in range(np+1)]
        path_upper = [0] + [[z] for z in circle_upper]
        pairs += deq.numerical_solution(ini, path_upper, eps,
                                        assume_analytic=True)
        # TODO: optimize case of real coefficients
        path_lower = [0] + [[z.conjugate()] for z in circle_upper]
        pairs += deq.numerical_solution(ini, path_lower, eps,
                                        assume_analytic=True)

    clock.toc()
    logger.info("Covered circle with %d squares, %s", num_sq, clock)
    return pairs

################################################################################
# Complete bound
################################################################################

def _coeff_zero(seqini, deq):
    """
    Find coefficients of generating function in the basis with these expansions
    at the origin

    INPUT:

    - seqini : list, initial terms of the sequence
    - deq : a linear ODE that the generating function satisfies

    OUTPUT:

    - coeff : vector, coefficients of generating function in the basis with
      these expansions at the origin
    """

    list_basis = deq.local_basis_expansions(0)
    list_coeff = []
    for basis in list_basis:
        mon = next(m for c, m in basis if not c == 0)
        if mon.k == 0 and mon.n >= 0:
            list_coeff.append(seqini[mon.n])
        else:
            list_coeff.append(0)
    return vector(list_coeff)

def _sing_in_disk(elts, rad, infinity):
    for j, x in enumerate(elts):
        mag = abs(x)
        if mag > rad:
            return elts[:j], mag
    return elts, infinity

def _choose_big_radius(all_exn_points, dominant_sing, next_sing_rad):
    max_smallrad = min(abs(ex - ds) for ds in dominant_sing
                                    for ex in all_exn_points
                                    if ex != ds)
    dom_rad = abs(dominant_sing[-1])
    # This should probably change to avoid smaller fake singularities
    rad = min(next_sing_rad*9/10 + dom_rad/10,
              dom_rad + max_smallrad*8/10)
    logger.info("Radius of large circle: %s", rad)
    return rad

def contribution_all_singularity(seqini, deq, singularities=None,
        known_analytic=[0], rad=None, total_order=1, min_n=50, halfside=None, prec_bit=53):
    """
    Compute a bound for the n-th element of a holonomic sequence

    INPUT:

    - seqini : list, initial elements of sequence, long enough to determine the
      sequence
    - deq : a linear ODE that the generating function satisfies
    - singularities : list of algebraic numbers, dominant singularities. If
      None, compute automatically
    - known_analytic : list of points where the generating function is known to
      be analytic, default is [0]
    - rad : radius of the big circle R_0. If None, compute automatically
    - total_order : integer, order to which the bound is computed
    - min_n : integer, bound is valid when n > max{N0, min_n}
    - halfside : real number, parameter to be passed on to numerical_sol_big_circle()
    - prec_bit : integer, numeric working precision (in bit)

    OUTPUT:

    - N0 : integer, bound is valid when n > max{N0, min_n}
    - bound : list of lists [rho, ser], where
        - rho are in QQbar
        - ser are symbolic expressions in variable 'n',
        - the sum of rho**(-n) * ser is a bound for the n-th element of a holonomic sequence
    """
    CB = ComplexBallField(prec_bit)
    RB = RealBallField(prec_bit)

    deq = DifferentialOperator(deq)

    # Interesting points = all sing of the equation, plus the origin
    all_exn_points = deq._singularities(QQbar, multiplicities=False)
    if not any(s.is_zero() for s in all_exn_points):
        all_exn_points.append(QQbar.zero())
    # Potential singularities of the function, sorted by magnitude
    if singularities is None:
        singularities = deq._singularities(QQbar, include_apparent=False,
                                           multiplicities=False)
    singularities = [s for s in singularities if not s in known_analytic]
    singularities.sort(key=lambda s: abs(s))
    logger.debug(f"potential singularities: {singularities}")

    # TODO: use numerical (ball) approximations instead of algebraic numbers
    if rad is None:
        dominant_sing, next_sing_rad = _sing_in_disk(singularities,
                abs(singularities[0]), abs(singularities[-1])*3)
        rad = _choose_big_radius(all_exn_points, dominant_sing, next_sing_rad)
    else:
        dominant_sing, _ = _sing_in_disk(singularities, rad,
                abs(singularities[-1])*2 + rad*2)
        if not dominant_sing:
            raise ValueError("No singularity in given disk")
        if abs(dominant_sing[-1]) == rad:
            raise ValueError("A singularity is on the given radius")
    logger.debug(f"dominant singularities: {dominant_sing}")

    # Make sure the disks B(ρ, |ρ|/n) do not overlap
    if len(dominant_sing) > 1:
        min_dist = min(abs(s0 - s1) for s0 in dominant_sing
                                    for s1 in dominant_sing
                                    if s0 != s1)
        N1 = ceil(2*abs(dominant_sing[-1])/min_dist)
    else:
        N1 = 0

    logger.debug(f"{N1=}")

    ini = _coeff_zero(seqini, deq)

    if halfside is None:
        halfside = min(abs(abs(ex) - rad) for ex in all_exn_points)/10
        logger.info("half-side of small squares: %s", halfside)
    pairs = numerical_sol_big_circle(deq, ini, dominant_sing, rad,
                                     halfside, prec_bit)
    coord_big_circle = [z for z, _ in pairs]
    f_big_circle = [f for _, f in pairs]
    max_big_circle = RB.zero()

    n = SR.var('n')
    bound = []
    list_val_bigcirc = []
    list_data = []
    list_max_kappa = []
    list_min_val_rho = []

    for rho in dominant_sing:
        list_val, list_bound, val_big_circle, max_kappa, min_val_rho = contribution_single_singularity(
                deq, ini, rho, rad, coord_big_circle, total_order,
                min_n, prec_bit = prec_bit)
        list_data.append((rho, list_val, list_bound))
        list_max_kappa.append(max_kappa)
        list_val_bigcirc.append(val_big_circle)
        list_min_val_rho.append(min_val_rho)

    final_kappa = max(list_max_kappa)
    final_val = min(list_min_val_rho)
    re_gam = - final_val - 1 #max([-val.real()-1 for val in list_val])
    v, logz, u, w, logn = list_data[0][2][0].parent().gens()

    for rho, list_val, list_bound in list_data:
        #bound += [
        #    SR(QQbar(1/rho)**n) * SR(n**QQbar(-val-1))
        #        * truncate_tail(poly_bound, poly_bound.degree(w), min_n, w, final_kappa, logn)(0,0,0, 1/n, log(n))
        #    for val, poly_bound in zip(list_val, list_bound)]
        bound.append([rho, sum([truncate_tail_SR(-val-1, poly_bound, re_gam - total_order, min_n, w, final_kappa, logn, n)
            for val, poly_bound in zip(list_val, list_bound)])])

    sum_g = [sum(v) for v in zip(*list_val_bigcirc)]
    for v in list_val_bigcirc:
        max_big_circle = max_big_circle.max(*(
            (s - vv).above_abs()
            for s, vv in zip(sum_g, v)))
    max_big_circle = max_big_circle.max(*(
        (s - vv).above_abs()
        for s, vv in zip(sum_g, f_big_circle)))
    #Simplify bound contributed by big circle
    M = RB(abs(dominant_sing[0]))
    rad_err = max_big_circle * (((CB(e) * (total_order - re_gam)
                  / (M/CB(rad)).log()).pow(RB(re_gam - total_order))
                 / CB(min_n).log().pow(final_kappa)) if re_gam <= total_order + min_n * (M/RB(rad)).log()
                else ((M/CB(rad)).pow(min_n) * CB(min_n).pow(total_order - re_gam)
                 / CB(min_n).log().pow(final_kappa)))
    #bound += [CB(0).add_error(rad_err) * (SR(QQbar(1/abs(dominant_sing[0]))**n)
    #                                      * SR(n**QQbar(re_gam)) * (SR(1/n)**total_order) * (SR(log(n))**final_kappa))]

    #Add big circle error bound
    list_rho = [rho for rho, _, _ in list_data]
    if abs(dominant_sing[0]) in list_rho:
        ind_rho_real = list_rho.index(abs(dominant_sing[0]))
        bound[ind_rho_real][1] += CB(0).add_error(rad_err) * SR(n**QQbar(re_gam - total_order)) * (SR(log(n))**final_kappa)
    else:
        bound += [[abs(dominant_sing[0]),
                   CB(0).add_error(rad_err) * SR(n**QQbar(re_gam - total_order)) * (SR(log(n))**final_kappa)]]
    #print(CB(0).add_error(rad_err) * (SR(QQbar(1/abs(dominant_sing[0]))**n)
    #                                      * SR(n**QQbar(re_gam)) * (SR(1/n)**total_order) * (SR(log(n))**final_kappa)))

    #Compute N0
    list_all_val = [val for _, lval, _ in list_data for val in lval]
    N0 = max(ceil(2.1 * (max([abs(val) for val in list_all_val]) + total_order + 1)), N1)

    return N0, bound

class FormalProduct:

    def __init__(self, exponential_factor, series_factor):
        self._exponential_factor = exponential_factor
        self._series_factor = series_factor

    def __repr__(self):
        return f"{self._exponential_factor}*({self._series_factor})"

    def exponential_factor(self):
        return self._exponential_factor

    def series_factor(self):
        return self._series_factor

    def expand(self):
        return self._exponential_factor*self._series_factor

def to_asymptotic_expansion(Coeff, name, term_data, n0):

    n_as_sym = SR.var(name)

    # XXX detect cases where we can use 1 or ±1 or U as Arg
    Exp, Arg = ExponentialGrowthGroup.factory(QQbar, name, return_factors=True)
    # AsymptoticRing does not split MonomialGrowthGroups with non-real
    # exponent groups in growth*non-growth parts, presumably because this has no
    # impact on term ordering. Let us do the same.
    Pow = MonomialGrowthGroup(QQbar, name)
    Log = MonomialGrowthGroup(ZZ, f"log({name})")
    Growth = cartesian_product([Arg, Exp, Pow, Log])
    # (n,) = Growth.gens_monomial()
    Asy = AsymptoticRing(Growth, coefficient_ring=Coeff)
    ET = Asy.term_monoid('exact')
    BT = Asy.term_monoid('B').change_parameter(
            coefficient_ring=Coeff._real_field())

    def make_arg_factor(dir):
        if dir.imag().is_zero() and dir.real() >= 0:
            return ET.one()
        else:
            return ET(Arg(raw_element=dir))

    rho0 = term_data[0][0]
    mag0 = abs(rho0)
    exp_factor = ET(Exp(raw_element=~mag0))
    if all(rho == rho0 for rho, _ in term_data[1:]):
        exp_factor *= make_arg_factor(~rho0)
    else:
        rho0 = mag0

    terms = []
    for rho, expr in term_data:
        dir = rho0/rho
        assert abs(dir).is_one() # need an additional growth factor otherwise
        arg_factor = make_arg_factor(dir)
        if expr.operator() == add_vararg:
            symterms = expr.operands()
        else:
            symterms = [expr]
        for symterm in symterms:
            term = arg_factor*ET(symterm.subs(n=n_as_sym))
            if term.coefficient.contains_zero():
                term = BT(term.growth, coefficient=term.coefficient.above_abs(),
                        valid_from={name: n0})
            terms.append(term)

    return FormalProduct(Asy(exp_factor), Asy(terms))


def bound_coefficients(deq, seqini, name='n', order=3, prec=53, n0=50, *,
        assume_analytic=[0], big_radius=None):

    n0bis, term_data = contribution_all_singularity(seqini, deq,
            known_analytic=assume_analytic, rad=big_radius, total_order=order,
            min_n=n0, prec_bit=prec)
    n0 = max(n0, n0bis)

    Coeff = ComplexBallField(prec)
    return to_asymptotic_expansion(Coeff, name, term_data, n0)


def eval_bound(bound, n_num, prec = 53):
    """
    Evaluation of a bound produced in contribution_all_singularity()
    """
    CBFp = ComplexBallField(prec)
    list_eval = [rho**(-n_num) * ser.subs(n = n_num) for rho, ser in bound]
    return CBFp(sum(list_eval))


# XXX test the tester!
def check_seq_bound(asy, ref, indices=None, *, verbose=False, force=False):
    r"""
    """
    Coeff = asy.parent().coefficient_ring
    myCBF = Coeff.complex_field()
    myRBF = myCBF.base()
    # An asymptotic ring with exponents etc. in CBF instead of QQbar, to make it
    # possible to evaluate a^n, n^b
    BGG = cartesian_product([
        ExponentialGrowthGroup.factory(myCBF, 'n',
                                       extend_by_non_growth_group=True),
        MonomialGrowthGroup.factory(myRBF, 'n',
                                    extend_by_non_growth_group=True),
        GrowthGroup('log(n)^ZZ')])
    BAsy = AsymptoticRing(BGG, myCBF)
    # XXX wrong results in the presence of complex exponents (#32500)
    basy = BAsy(asy, simplify=False)
    exact_part = basy.exact_part()
    error_part = basy.error_part()
    assert len(error_part.summands) == 1
    bterm = error_part.summands.pop()
    assert isinstance(bterm, BTerm)
    error_ball = myCBF.zero().add_error(bterm.coefficient)
    (name,) = asy.variable_names()
    validity = bterm.valid_from[name]
    if indices is None:
        try:
            rb = int(len(ref))
        except TypeError:
            rb = validity + 10
        indices = range(validity, rb)
    for n in indices:
        if n < validity and not force:
            continue
        bn = myRBF(n)
        one = myRBF.one()
        refval = ref[n]
        asyval = exact_part.substitute({name: bn})
        err0 = bterm.growth._substitute_({name: bn, '_one_': one})
        relbound = (asyval - refval)/err0
        if relbound not in error_ball:
            absbound = asyval + error_ball*err0
            if absbound.contains_exact(refval):
                # this may be a false warning due to overestimation at
                # evaluation time
                print(f"{name} = {n}, magnitude of interval rescaled "
                        f"error {relbound} is larger than {bterm.coefficient}")
            else:
                # definitely wrong
                msg = (f"{name} = {n}, computed enclosure "
                        f"{absbound} does not contain reference value {refval}"
                        f" ≈ {myCBF(refval)}")
                if force:
                    print(msg)
                else:
                    raise AssertionError(msg)
        else:
            if verbose:
                print(f"{name} = {n}, {relbound} contained in {error_ball}")
