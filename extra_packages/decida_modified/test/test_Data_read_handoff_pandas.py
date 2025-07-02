#!/usr/bin/env python
from __future__ import print_function
import decida
import decida.test
import pandas as pd
from decida.Data import Data
from decida.DataViewm import DataViewm

test_dir = decida.test.test_dir()

df = pd.read_csv(test_dir + "data/data.csv", skiprows=1)

d = Data()
d.read_numpy_arrays(df.values, cols=list(df.columns))

names = d.names()
values = d.values()

df1 = pd.DataFrame(data=values, columns=names)
print("df1 = ", df1)
