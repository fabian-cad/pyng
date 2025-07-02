#!/usr/bin/env python
import decida
import decida.test
import pandas as pd
from decida.Data import Data
from decida.DataViewm import DataViewm

test_dir = decida.test.test_dir()

df = pd.read_csv(test_dir + "data/data.csv", skiprows=1)

d = Data()
d.read_numpy_arrays(df.values, cols=list(df.columns))
DataViewm(data=d)
