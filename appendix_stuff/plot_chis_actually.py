#/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 12:00:20 2019

@author: janne
"""
import numpy as np
import os
import matplotlib.pyplot as plt

plt.close("all")
Log_L_obs = 1.305
Log_Teff_obs = 3.839
Log_g_obs = 3.6
Log_Teff_obs_unc = 0.007
Log_L_obs_unc = 0.065 
Log_g_obs_unc = 0.1
#final_list = []
minimums       = []

list_of_files  = []
list_of_masses = []
list_of_zs     = []
list_of_ys     = []
list_of_mlts   = []
list_of_ovs    = []
list_of_pnums  = []
#filename = '/home/janne/Gunter_project/gunther_project/Results_l0/final_LOGS-1.75-0.03-0.75-0.2-0.3.txt'
def getminimum(filename):
    final_list = []
    inner_list = []
    with open(filename) as f:
        for line in f:
            inner_list = [elt.strip() for elt in line.split(',')]
            final_list.append(inner_list)
    #print(filename)
    chis      = []
    best_pnums = []
    teffs     = []
    ls        = []
    gs        = []

    for i in range(0,len(final_list)):
        #fund     = float(final_list[i][0])
        #first    = float(final_list[i][1])
        pnum     = float(final_list[i][7])
        #print(pnum)
        teff     = float(final_list[i][8])
        g        = float(final_list[i][9])
        l        = float(final_list[i][10])
        #age      = float(final_list[i][11])
        mass     = float(final_list[0][2])
        z        = float(final_list[0][3])
        y        = float(final_list[0][4])
        mlt      = float(final_list[0][5])
        ov       = float(final_list[0][6])
        chi      = float(final_list[i][19])

        chis          += [chi]
        best_pnums    += [pnum]
        teffs         += [teff]
        ls            += [l]
        gs            += [g]

    a = np.asarray(chis)
    b = np.asarray(best_pnums)
      
    minimum = min(a)
     
    #print(a,minimum)
    pnum_index = np.where(a==minimum)
    #print(pnum_index)
    #print(best_pnums)
    #print(best_pnums)
    pnum_best = b[pnum_index]

    return minimum, mass, z, y, mlt, ov, pnum_best
profile_structure = []
list_of_minimums = []
for root, dirs, files in sorted(os.walk('/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid/new_Results_l0')):
        dirs.sort(key=lambda x: '{0:0>20}'.format(x))    
        for file in files:
            if file.startswith("final_"):
                filedir = os.path.join(root,file)
                #print(filedir)
                minimum, mass, z, y, mlt, ov, pnum = getminimum(filedir)
                list_of_files    += [filedir]
 

                list_of_pnums    += [pnum]
                list_of_minimums += [minimum]
                list_of_masses   += [mass]
                list_of_zs       += [z]
                list_of_ys       += [y]
                list_of_mlts     += [mlt]
                list_of_ovs      += [ov]
                
                profile_structure += ['LOGS-'+ str(format(mass, '.2f')) + '-'+ str(z) + '-' + str(y) + '-' 
                                      + str(mlt) +'-'+ str(ov) + '-'+ 'profile' +str(int(pnum)) +'.data']
                
                decent = np.asarray([list_of_minimums, list_of_files, list_of_pnums, list_of_masses,
                                     list_of_zs, list_of_ys, list_of_mlts, profile_structure])
                #print(decent) 
#print(list_of_pnums)
fivep_index = np.argsort(decent[0,:].astype('float'))
sorted_min  = np.asarray(decent[:,[fivep_index]])
#print(sorted_min)
percentage = 0.05

fivep = sorted_min[:,:,0:int(percentage*len(list_of_minimums))]
final = np.concatenate(fivep)

fig = plt.figure()
ax = plt.gca()

plt.plot(list_of_masses, list_of_minimums,'k.', MarkerSize = 15)
plt.plot(final[3,:].astype('float'), final[0,:].astype('float'), 'r.',fillstyle='none', MarkerSize = 15,markeredgewidth=3)
plt.xticks(np.arange(min(list_of_masses)-0.05, max(list_of_masses)+0.05, step=0.02))
ax.tick_params(labelsize = 20)
#print(min(list_of_masses), max(list_of_masses))
Mlabel = r'$M/M_{\odot}$'
Mltlabel = r'$\alpha_{mlt}$'
Zlabel = r'$Z$'
Ylabel = r'$Y$'
OVlabel = r'$\alpha_{ov}$'
plt.xlabel(Mlabel,fontsize=20)
plt.ylabel(r'$\chi^{2}$', fontsize=20)        
limit = (5/100)*max(list_of_minimums) + min(list_of_minimums)
plt.xticks(np.arange(1.45, 2.25, step=0.05))
#print(final)
firstpoint = np.float(final[0,-1])
secondpoint = np.float(sorted_min[0][0][len(final[0])])
mean = np.mean([firstpoint, secondpoint])

plt.plot([1.49,max(list_of_masses)+0.01],[mean,mean],'r--', linewidth = 3.50)
final_needed = []
files3 = []
for k in range(0,len(final[1])):
    y = 0
    directories = final[1][k]
    files  = directories.lstrip('/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid/new_Results_l0/')
    pnumber = str(int(float(final[2][k])))
    pnums = 'profile' + pnumber + '.data' 
    files2 = files.rstrip('.txt')
    files3 += [files2 + '-profile' + str(final[2,y])]
    y += 1
    final_needed += [[files, pnums ]]
    
np.savetxt('/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid/new_Results_l0/bestfivep.txt', final_needed, delimiter=",", newline = "\n", fmt="%s")


    #best_files = [files2]
#allinfonames = files2 
#plt.plot(list_of_masses[indx], list_of_minimums[indx], 'r.', MarkerSize = 25 )

## find top 5% models based on Teff, L, and Logg.

plt.show() 
