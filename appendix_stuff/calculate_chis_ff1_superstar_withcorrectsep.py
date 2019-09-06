#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 21:45:41 2019

@author: janne
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 17:29:08 2019

@author: janne

#calculate chi2 for one directory
"""

import numpy as np
import os
import re
import gyre_output_read as gar
radial_funda = 6.8980
radial_first = 8.9606

#The following uncertainties are incorrect! - Discuss with Vichi what to do 
#radial_funda_unc = 3.682937895*10**(-5) #2.762223525*10**(-7)
#radial_first_unc = 1.172368430*10**(-5) #8.454940424*10**(-7)

Log_L_obs = 0.859073 # GAIA 0.8372440 self-calculated
Log_Teff_obs = 3.87506
Log_g_obs = 3.9
Log_Teff_obs_unc = 0.01158
Log_L_obs_unc = 0.00328 # GAIA 
Log_g_obs_unc = 0.2
sepa_obs = 3.5 #cyc/day
sepa_obs_unc = 0.05
#seps = []

def getmeansep(fname):
    fnumbers = []
    alle = []
    finalone = []
    for root, dirs, files in sorted(os.walk(fname)):
            #files.sort(key=lambda x: int(os.path.splitext(x)[0])) 
            for file in files:
                
                if not file.endswith('freqs.dat'):
                    continue 
#              	print(file)
                
                fdires = os.path.join(root,file)
                fdata = gar.readmesa(fdires)
#                #print(fdires)
                
                if np.size(fdata) == 1:
                    continue
                
                fnum = re.search('profile(.+?)-freqs.dat', fdires)
                        
                if fnum: 
                    fnums = fnum.group(1)
                    fnum2 = int(fnums)
                    #print(fnum2)
#                if not fnum2 > 900:
#                    continue
                allf = []   
                for i in range(0,len(fdata)):
                    if i < len(fdata) -1:
                        separation = np.abs(fdata[i+1][4]-fdata[i][4])
                        
                    else:
                        separation = np.abs(fdata[i-1][4]-fdata[i][4])
                    
                    
                    allf += [separation]
                #rint(separation)
                #The following way of determining mean applies only well to l=0 modes!
               
                meansep = np.mean(allf)
                finalone += [[meansep, fnum2]]
                finalonearray = np.asarray(finalone)
                finalonearray = finalonearray[finalonearray[:,1].argsort()]
    #print(finalonearray)
    return finalonearray



def getchis(filename,result_name):
#    filename = '/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid_superstar/Results_l0/results.txt'
    
    final_list = []
    total_chi = []
    red_chi = []
    with open(filename) as f:
        for line in f:
            inner_list = [elt.strip() for elt in line.split(',')]
            final_list.append(inner_list)
            
    sepa_info = []
    f_sepas = []
    seps = [] 
    pnums = []
    print(filename)
    hoveddir = '/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid_superstar/' 
    logdir = hoveddir + filename.strip('/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid_superstar/Results_l0/final_').rstrip('.txt')
    #print(logdir)
    finalforsep = getmeansep(logdir)
    print(np.shape(finalforsep), len(finalforsep))
    #print(finalforsep[0][0])    
    sepaarray = np.asarray(finalforsep)
    for i in range(0,len(final_list)):
        
        pnum     = float(final_list[i][6]) 
        print(pnum, finalforsep[i][1])
        sepa     = float(finalforsep[i][0])
        teff     = float(final_list[i][7])
        g        = float(final_list[i][8])
        l        = float(final_list[i][9])
        age      = float(final_list[i][10])
        seps     += [sepa] 
        pnums    += [pnum]
        ########## METHOD 1 ###################################
         
        if not int(pnum) > 900:
           continue

        if i>0:
           delta_sep = np.abs(float(final_list[i][0])-float(final_list[i-1][0]))
        elif i==0:
           delta_sep = np.abs(float(final_list[i][0])-float(final_list[i+1][0]))
        
        f_sep = delta_sep/sepa_obs_unc
        
        alpha = 1
        chi_sep           = (np.abs(sepa - sepa_obs)/sepa_obs_unc)**2   #*f_sep)
        chi_sep_pumped    = (sepa - sepa_obs)**2/(sepa_obs_unc**2*f_sep)
        chi_allsep        = 1/alpha*chi_sep  
        chi_teff          = ((teff-Log_Teff_obs)/Log_Teff_obs_unc)**2
        chi_g             = ((g-Log_g_obs)/Log_g_obs_unc)**2
        chi_l             = ((l-Log_L_obs)/Log_L_obs_unc)**2
        
        chi_rest   = (chi_teff + chi_g + chi_l) # + chi_sep)
        ratio      = chi_rest/chi_allsep
        #print(chi_allsep, chi_rest)
#        chi_final         = chi_sep + chi_rest

        sepa_info += [[ratio, f_sep, chi_rest, chi_sep, chi_sep_pumped, chi_l, sepa]] 
    index_forfinal = np.where(np.asarray(pnums) > 900)
    index_forfinal2 = np.asarray(index_forfinal)
    finallist_array = np.asarray(final_list)
    sepa_info_array = np.asarray(sepa_info)

    ratios         = np.asarray(sepa_info_array[:,0])
    functs         = np.asarray(sepa_info_array[:,1])
    rests          = np.asarray(sepa_info_array[:,2])
    allseps        = np.asarray(sepa_info_array[:,3])
    allseps_pumped = np.asarray(sepa_info_array[:,4])
    ls             = np.asarray(sepa_info_array[:,5])
    just_seps      = np.asarray(sepa_info_array[:,6])
    
    add_factor = np.sum(ratios)/len(ratios)
    #print(add_factor)
    new_chi_sepa = allseps #*(add_factor)
    final_chi    = new_chi_sepa + rests
    final_chi_pumped = allseps_pumped + rests
#    print(type(final_list),np.shape(final_list), type(index_forfinal2), np.shape(index_forfinal2))
    output_chi = np.column_stack((ratios, functs, rests, allseps, allseps_pumped, ls,  final_chi, final_chi_pumped, just_seps))
    #print(len(finallist_array[index_forfinal[0],:]), len(output_chi), len(index_forfinal[0]))
    output_final = np.column_stack((finallist_array[index_forfinal2[0],:], output_chi))
    #print(rests[0], allseps[0], final_chi[0], just_seps[0]) 
    np.savetxt(result_name, output_final, delimiter=",", newline = "\n", fmt="%s")
    
    return output_final

for root, dirs, files in sorted(os.walk('/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid_superstar/Results_l0')):
    for file in files:
        if file.startswith('final'):
            dirs = os.path.join(root,file)
            maindir = '/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid_superstar/new_Results_l0'
            #logdir = maindir.rstrip('new_Results_l0') + dirs.lstrip(maindir).strip('_final-').rstrip('.txt')
            output_filename = maindir + '/' + os.path.join(file)
            output_final = getchis(dirs,output_filename)
            

