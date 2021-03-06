import torch
import math
from torch.autograd import Variable
from torch.nn import Parameter
from gpytorch.math.functions import LogNormalCDF


def test_forward():
    inputs = torch.Tensor([-6, -5, -3, -1, 0, 1, 3, 5])
    output = LogNormalCDF()(Variable(inputs)).data

    # Answers should be reasonable for small values
    assert(math.fabs(output[0] + 20.7368) < 1e-4)
    assert(math.fabs(output[1] + 15) < 0.15)
    assert(math.fabs(output[2] + 6.6) < 0.1)
    assert(math.fabs(output[3] + 1.841) < 0.001)

    # Should be very accurate for positive values
    assert(math.fabs(output[4] + 0.693147) < 1e-4)
    assert(math.fabs(output[5] + 0.1727) < 1e-4)
    assert(math.fabs(output[6] + 0.00135081) < 1e-4)
    assert(math.fabs(output[7] + 2.86652e-7) < 1e-4)


def test_backward():
    inputs = Parameter(torch.Tensor([-6, -5, -3, -1, 0, 1, 3, 5]))
    output = LogNormalCDF()(inputs)
    output.backward(torch.ones(8))

    gradient = inputs.grad.data
    expected_gradient = torch.Tensor([6.1585, 5.1865, 3.2831, 1.5251, 0.7979, 0.2876, 0.0044, 0.0000])

    # Should be reasonable for small values
    assert(all(torch.abs(gradient[:3] - expected_gradient[:3]) < 5e-1))

    # Should be very accurate for larger ones
    assert(all(torch.abs(gradient[3:] - expected_gradient[3:]) < 5e-4))
