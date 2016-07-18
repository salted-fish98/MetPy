# Copyright (c) 2008-2015 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import division

import pytest

from metpy.gridding.gridding_functions import (calc_kappa,
                                               remove_observations_below_value,
                                               remove_nan_observations,
                                               remove_repeat_coordinates,
                                               interpolate)

import numpy as np

from scipy.spatial.distance import cdist

from numpy.testing import assert_array_almost_equal, assert_almost_equal

from metpy.cbook import get_test_data


@pytest.fixture()
def test_coords():
    x = np.array([8, 67, 79, 10, 52, 53, 98, 34, 15, 58], dtype=float)
    y = np.array([24, 87, 48, 94, 98, 66, 14, 24, 60, 16], dtype=float)

    return x, y


def test_calc_kappa(test_coords):
    r"""Tests calculate kappa parameter function"""

    x, y = test_coords

    spacing = np.mean((cdist(list(zip(x, y)),
                             list(zip(x, y)))))

    value = calc_kappa(spacing)

    truth = 5762.6872048

    assert_almost_equal(truth, value, decimal=6)


def test_remove_observations_below_value(test_coords):
    r"""Tests threshold observations function"""

    x, y = test_coords[0], test_coords[1]

    z = np.array(list(range(-10, 10, 2)))

    x_, y_, z_ = remove_observations_below_value(x, y, z, val=0)

    truthx = np.array([53, 98, 34, 15, 58])
    truthy = np.array([66, 14, 24, 60, 16])
    truthz = np.array([0, 2, 4, 6, 8])

    assert_array_almost_equal(truthx, x_)
    assert_array_almost_equal(truthy, y_)
    assert_array_almost_equal(truthz, z_)


def test_remove_nan_observations(test_coords):
    r"""Tests remove observations equal to nan function"""

    x, y = test_coords[0], test_coords[1]

    z = np.array([np.nan, np.nan, np.nan, 1, 1, 1, 1, 1, 1, 1])

    x_, y_, z_ = remove_nan_observations(x, y, z)

    truthx = np.array([10, 52, 53, 98, 34, 15, 58])
    truthy = np.array([94, 98, 66, 14, 24, 60, 16])
    truthz = np.array([1, 1, 1, 1, 1, 1, 1])

    assert_array_almost_equal(truthx, x_)
    assert_array_almost_equal(truthy, y_)
    assert_array_almost_equal(truthz, z_)


def test_remove_repeat_coordinates(test_coords):
    r"""Tests remove repeat coordinates function"""

    x, y = test_coords

    x[0] = 8.523
    x[-1] = 8.523
    y[0] = 24.123
    y[-1] = 24.123

    z = np.array(list(range(-10, 10, 2)))

    x_, y_, z_ = remove_repeat_coordinates(x, y, z)

    truthx = np.array([8.523, 67, 79, 10, 52, 53, 98, 34, 15])
    truthy = np.array([24.123, 87, 48, 94, 98, 66, 14, 24, 60])
    truthz = np.array([-10, -8, -6, -4, -2, 0, 2, 4, 6])

    assert_array_almost_equal(truthx, x_)
    assert_array_almost_equal(truthy, y_)
    assert_array_almost_equal(truthz, z_)


def test_interpolate(test_coords):
    r"""Tests main interpolate function"""

    xp, yp = test_coords

    xp *= 10
    yp *= 10

    z = np.array([0.064, 4.489, 6.241, 0.1, 2.704, 2.809, 9.604, 1.156,
                  0.225, 3.364])

    __, __, img = interpolate(xp, yp, z, hres=10,
                              interp_type='natural_neighbor')

    truth = np.load(get_test_data("nn_test.npz"))['img']

    assert_array_almost_equal(truth, img)

    __, __, img = interpolate(xp, yp, z, hres=10, search_radius=200,
                              minimum_neighbors=1, interp_type='cressman')

    truth = np.load(get_test_data("cress_test.npz"))['img']

    assert_array_almost_equal(truth, img)

    __, __, img = interpolate(xp, yp, z, hres=10, search_radius=400,
                              minimum_neighbors=1, interp_type='barnes')

    truth = np.load(get_test_data("barnes_test.npz"))['img']

    assert_array_almost_equal(truth, img)

    __, __, img = interpolate(xp, yp, z, hres=10, interp_type='linear')

    truth = np.load(get_test_data("linear_test.npz"))['img']

    assert_array_almost_equal(truth, img)

    __, __, img = interpolate(xp, yp, z, hres=10, interp_type='nearest')

    truth = np.load(get_test_data("nearest_test.npz"))['img']

    assert_array_almost_equal(truth, img)

    __, __, img = interpolate(xp, yp, z, hres=10, interp_type='cubic')

    truth = np.load(get_test_data("cubic_test.npz"))['img']

    assert_array_almost_equal(truth, img)

    __, __, img = interpolate(xp, yp, z, hres=10, interp_type='rbf')

    truth = np.load(get_test_data("rbf_test.npz"))['img']

    assert_array_almost_equal(truth, img)
