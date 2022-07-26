import numpy as np
from scipy.integrate import solve_ivp
import scipy


def negative_derivatives(x, y, H, A, Ms):
    '''return the derivatives of the system of equations describing the theta(x),
    where 0 is taken to be the edge of the layers and d is the interface'''
    dw = (H*Ms)/(2*A*10)*np.sin(y[0])
    dtheta = y[1]
    if dw == 0 and dtheta == 0:
        # known unstable solution give nudge
        dw += 1e-7
    return -np.array([dtheta, dw])


def negative_boundary_conditions(theta, w, J1, J2, A):
    '''returns the residuals of the boundary condition at the interface of the
    device'''
    return np.sum(-2*A*10*w[-1] - J1*np.sin(2*theta[-1]) - J2*np.sin(4*theta[-1]))


@np.vectorize
def shoot(theta0, H, J1, J2, A, Ms, half_thickness):
    '''function to be minimized by the shooting method, this function solves theta
    equation for the set of parameters given and returns the residuals'''
    tspan = (0, half_thickness)
    x = np.linspace(0, half_thickness, 1000)
    sol = solve_ivp(negative_derivatives, tspan, [theta0, 0], args=[H, A, Ms],
                    t_eval=x, rtol=1e-8)
    theta = sol.y[0]
    w = sol.y[1]
    return negative_boundary_conditions(theta, w, J1, J2, A)


def fit_function(fields, J1, J2, A, Ms, half_thickness, zero_bound=1e-4, sorted=True):
    '''fitting function for the shooting solution, FIELDS MUST BE IN ASCENDING
    ORDER IF sorted=True this allows for massive speed up in run time'''
    # initialize array for storing return array
    mag = np.zeros(len(fields))
    x = np.linspace(0, half_thickness, int(half_thickness*10))
    
    if J1 < 2*J2:
        upper_bound = 1/2*np.arccos(-J1/(2*J2))
    else:
        upper_bound = np.pi/2
        
    for index, H in enumerate(fields):

        # upon nearing saturation the solution becomes zero the solver requires
        # a point on either side of axis so this causes
        # error the except handles and sets theta0 to zero because we are at saturation
        try:
            theta0 = scipy.optimize.brentq(shoot,
                                           zero_bound,
                                           upper_bound,
                                           xtol=1e-4,
                                           args=(H, J1, J2, A, Ms, half_thickness))
        except ValueError:
            theta0 = 0

        # range to solve the equation over
        tspan = (0, max(x))
        sol = solve_ivp(negative_derivatives, tspan, [theta0, 0],
                        args=[H, A, Ms], t_eval=x, rtol=1e-5)
        thetas_opt = sol.y[0]
        value = 1/(len(x))*sum(np.cos(thetas_opt))
        mag[index] = value
        if sorted:
            upper_bound = theta0
        if 1 - value < 1e-4:
            # if we reached saturation no reason to continue computing
            mag[index:] = 1
            break
    return mag
