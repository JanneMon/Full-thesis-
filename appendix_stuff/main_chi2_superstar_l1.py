#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 16:02:42 2019

@author: janne
main_chi2_superstar_l1
"""
import os
import matplotlib.pyplot as plt
import make_table_initparams_superstar as init
#import make_table_fundfirst as fund
import get_l0fromseparation_superstar as sep
import calculate_chis_ff1_superstar_actually as chi
import numpy as np
#import natsort as ns
plt.close('all')
print('Heeeeeeej')

def firstpart(dirname):
    list_of_names = []
    list_of_minimums = []
    #savenames = []
    runonce = 0
    for root, dirs, files in sorted(os.walk(dirname)):
        #dirs.sort(key=lambda x: '{0:0>20}'.format(x))    
        for dire in dirs:
            if dire.startswith('LOGS'):
                #plt.figure(dire)
                directories = os.path.join(root,dire)
                print(directories, runonce)
                name = directories.lstrip(root)   
                names = '/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid_superstar/Results_l0/final_'+ name + '.txt'
            
                sep.getfundfreqs(directories)
                #print(directories)
                init.getinitparams(directories)
            
                total_chi, minimum = chi.getchis(names)
            #list_of_names += [names]
            #list_of_minimums += [minimum]
        
            #print(list_of_names)
            #fullnamelist = "namelist_" + mtracks + ".txt"
            #savenames += [fullnamelist]

            runonce += 1
            
    #np.savetxt('allnames.txt', savenames, delimiter=",", newline = "\n", fmt="%s")
    
    return
startpath = '/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid_superstar/'
list_of_dirs = ['m155','m160','m170','m180','m190','m200','m220'] #some 180 dirs did not work!
for i in list_of_dirs:
        
   firstpart(startpath + i)
