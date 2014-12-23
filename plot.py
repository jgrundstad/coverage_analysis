import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

infile = sys.argv[1]
df = pd.read_csv(infile, sep='\t')
plots = []

for header in list(df.columns.values)[1:]:
  plots.append(plt.plot(df[header]))

#plt.ylim([0,100])
plt.xlabel('Window #')
plt.ylabel('Coverage')
plt.legend(list(df.columns.values)[1:])
plt.show()
