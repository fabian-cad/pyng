#!/usr/bin/env python
import numpy as np
from decida.Data import Data
from decida.DataViewm import DataViewm

t = np.linspace(0, 4*2*np.pi, 1000)
sin = np.sin(t)
cos = np.cos(t)

d = Data()
d.read_numpy_arrays(t, sin, cos, cols=("t", "sin", "cos"))
DataViewm(data=d, command=[["t sin cos"]])
