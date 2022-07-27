# MagnetizationFitting

This repository looks to model magnetic moment distribution using a continuous approximation obeying:

$$\theta^{~\prime\prime} = \frac{\text{sin}\theta}{\delta^2}$$

where $\theta$(x) is the angle between the magnetic moment and the external magnetic field as a function of distance from the edge of the device 

$$\delta^2 = \frac{HM_s}{2A}$$

where $H$ is the external magnetic field,  $A$ is the exchange stiffness

with boundary conditions 

$$\theta^{~\prime}(0) = 0$$

$$-2A\theta^{~\prime}(d) - J_1\text{sin}(2\theta(d)) - J_2\text{sin}(4\theta(d))$$

where $J_1$ is the Bilinear interlayer exchange and $J_2$ is the Biquadratic interlayer exchange coupling, $\textcolor{orange}{\underline{\text{\small both are defined as positive}}}$, d is the distance to the interface.

In this work we solve this using a hand written shooting method for solving BVPs in order to get the desired stability and speed, this makes the function
compatible with scipy.optimize.curve_fit for ease of use

# Examples

see the notebook folder for templates on how to use these functions to fit magnetization data, as well as an example of the discrete method of solving
that utilizes minimization.
