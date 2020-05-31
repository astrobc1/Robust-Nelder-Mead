import numpy as np
from neldermead.neldermead import NelderMead
from optimparameters import parameters as Parameters
import matplotlib.pyplot as plt

def gauss(pars, x):
    return pars['amp'].value * np.exp(-0.5 * ((x - pars['mu'].value) / pars['sig'].value)**2)

def optimize_gauss(pars, x, data):
    model = gauss(pars, x)
    rms = np.nansum((data - model)**2 / data.size)**0.5
    
    # Return value to minimize, and constraint (constraint = g(x) > 0)
    # Here we return 1 since this model does not utilize a constraint.
    return rms, 1


# An x grid
x = np.arange(-30, 30, .01)

# The "true" parameters and Gaussian
true_pars = Parameters.Parameters()
true_pars.add_parameter(Parameters.Parameter(name='amp', value=0.8))
true_pars.add_parameter(Parameters.Parameter(name='mu', value=2.3))
true_pars.add_parameter(Parameters.Parameter(name='sig', value=4.7))
true_gauss = gauss(true_pars, x)

true_gauss_noisy = np.copy(true_gauss)

# Make a noisy version
true_gauss = np.copy(true_gauss)
for i in range(true_gauss.size):
    true_gauss_noisy[i] = true_gauss[i] + (np.random.randn() / 100)

# A simple guess
guess_pars = Parameters.Parameters()
guess_pars.add_parameter(Parameters.Parameter(name='amp', value=2.2))
guess_pars.add_parameter(Parameters.Parameter(name='mu', value=-1.1))
guess_pars.add_parameter(Parameters.Parameter(name='sig', value=1.9))
guess_guass = gauss(guess_pars, x)

# Optimize the model from the starting guess
solver = NelderMead(optimize_gauss, guess_pars, args_to_pass=(x, true_gauss_noisy))
opt_result = solver.solve()

# Extract the best fit pars and plot the result
best_fit_pars = opt_result[0]

gauss_best_fit = gauss(best_fit_pars, x)


plt.plot(x, true_gauss_noisy, label='Noisy Data', marker='.', c='orange', lw=0)
plt.plot(x, guess_guass, label='Guess', ls=':', lw=2)
plt.plot(x, gauss_best_fit, label='Best Fit Model', c='black', lw=2)
plt.legend(loc='upper right')
plt.show()