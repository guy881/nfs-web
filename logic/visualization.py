import numpy as np
import scipy.io
mat_contents = scipy.io.loadmat('/home/stevens/Desktop/praca_inż/materiały/wizualizacja/NFS.mat')

x = mat_contents['x'].flatten()
y = mat_contents['y'].flatten()
z = mat_contents['z'].flatten()

e = mat_contents['E']
final_e = np.add.reduce(np.add.reduce(e, 3), 2)  # reduced by frequency and z (accumulated chart)
