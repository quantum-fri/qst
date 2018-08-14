import matplotlib.pyplot as plt
import sys, os
path = "C:\\Users\\quantum\\Desktop\\QST experiments\\Programs\\"
sys.path.append(path)
import Jul13QstFunctions as qst
import glob

angle = 0
data = [[],[],[]]

for filename in glob.glob(os.path.join(os.getcwd(), '*.txt')):
   #print(filename, "\n")
   name = os.path.basename(filename)
   quarter = int(name.split('-')[0])
   half = int(name.split('-')[1].split(".")[0])
   stats = qst.getMeanVar(filename)
   if(quarter != 0):
       data[0].append(stats[0])
       data[1].append(quarter)
   else:
       data[0].append(stats[0])
       data[1].append(half)

#Half Waveplate
plt.plot(data[1][0:12], data[0][0:12], color='r', marker='o', linestyle='', label='Half Waveplate')
#Quarter Waveplate
plt.plot(data[1][12:], data[0][12:], color='b', marker='o', linestyle='', label='Quarter Waveplate')
plt.ylabel('Avg. Photon Count')
plt.xlabel('Angle')
plt.legend(loc='upper left')
plt.show()