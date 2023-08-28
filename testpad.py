#%%
from read_data_func import *
import matplotlib.pyplot as plt
import glob
import os
# %%
files = sorted(glob.glob("test_data/*.txt"), key=os.path.getmtime)
print(files)

for i in files:
    if 'MSgate' in i:
        plt.figure()
        x, y1, err1, y2, err2 = get_MSgate_conincidence(i, ["middle", "right"])
        labels = ['gg', 'ee', 'eg+eg']
        for k in range(len(y2)):
            plt.errorbar(x, y2[k], err2[k], label = labels[k])
            plt.title(i[-9:-4])
            plt.legend()
# %%
