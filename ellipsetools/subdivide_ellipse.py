from ellipsetools.ellipse import Ellipse

import numpy as np
from scipy.optimize import minimize
from numpy.typing import NDArray

from typing import Tuple
import math


def arc_length_loss_function(theta: float, ellipse: Ellipse, arc_subdiv: float, r: float) -> float:
    dist, _ = ellipse.arc_length(r, theta)

    # MSE estimator
    return (dist - arc_subdiv) ** 2


def subdivide_ellipse(ellipse: Ellipse, N: int) -> Tuple[NDArray[np.float], NDArray[np.float]]:
    a = ellipse.a
    b = ellipse.b

    total_rad = 2 * math.pi
    radian_per_hole = total_rad / N

    ellipse = Ellipse(a, b)
    arc_length, _ = ellipse.arc_length()
    arc_subdiv = arc_length / N

    # Knowing the size of each arc length, we must now segment the ellipse.
    t = 0
    x, y = ellipse.point(t)
    x_coords = [x]
    y_coords = [y]
    ts = []
    for _ in range(N - 1):
        # Estimate of next t-value
        t_prime = t + radian_per_hole

        # Find a segment (t, t_prime) whose arc length is equal to arc_subdiv by optimization.
        optim = minimize(arc_length_loss_function, t_prime,
                         args=(ellipse, arc_subdiv, t))
        t = optim.x[0]
        ts.append(t)

        x, y = ellipse.point(t)
        x_coords.append(x)
        y_coords.append(y)

    return np.array(x_coords), np.array(y_coords)