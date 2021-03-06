from gpytorch.math.functions import AddDiag
from gpytorch.random_variables import GaussianRandomVariable
from .likelihood import Likelihood


class GaussianLikelihood(Likelihood):
    def forward(self, input, log_noise):
        assert(isinstance(input, GaussianRandomVariable))
        mean, covar = input.representation()
        noise = AddDiag()(covar, log_noise.exp())
        return GaussianRandomVariable(mean, noise)
