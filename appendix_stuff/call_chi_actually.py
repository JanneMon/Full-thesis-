#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 17:29:08 2019

@author: janne

#calculate chi2 for one directory
"""

import numpy as np
import os

radial_funda = 6.8980210
radial_first = 8.9606205

#The following uncertainties are incorrect! - Discuss with Vichi what to do 
radial_funda_unc = 7.432077540*10**(-7) #3.682937895*10**(-5) #2.762223525*10**(-7)  # Where does the first uncertainty come from?
radial_first_unc = 2.243216851*10**(-6) #1.172368430*10**(-5) #8.454940424*10**(-7)  # same

Log_L_obs = 1.305
Log_Teff_obs = 3.839
Log_g_obs = 3.6
Log_Teff_obs_unc = 0.007
Log_L_obs_unc = 0.065 
Log_g_obs_unc = 0.1


def getchis(filename, result_name):
    #filename = '/home/janne/Gunter_project/gunther_project/Results_l0/results.txt'
    
    final_list = []

    with open(filename) as f:
        for line in f:
            inner_list = [elt.strip() for elt in line.split(',')]
            pnum = float(inner_list[7])
            if pnum <= 900:
                continue
            final_list.append(inner_list)
            
    #print(len(final_list[0]))
    freqs_info = []

    for i in range(0,len(final_list)):
        #print(i)
        fund     = float(final_list[i][0])
        first    = float(final_list[i][1])
   #     mass     = float(final_list[i][2])
    #    z        = float(final_list[i][3])
    #    x        = float(final_list[i][4])
    #    mlt      = float(final_list[i][5])
   #     ov       = float(final_list[i][6])
        pnum     = float(final_list[i][7])
        teff     = float(final_list[i][8])
        g        = float(final_list[i][9])
        l        = float(final_list[i][10])
        age      = float(final_list[i][11])
   #    chi       = float(final_list[i][12])
   #    red_chi   = float(final_list[i][13])
   #    loglikely = float(final_list[i][14])
   
        assert pnum > 900
        ##### FIRST METHOD! ###########################################################
        if i > 0:
            delta_funda_j = np.abs(float(final_list[i][0])-float(final_list[i-1][0]))
            delta_first_j = np.abs(float(final_list[i][1])-float(final_list[i-1][1]))
        elif i == 0:
            delta_funda_j = np.abs(float(final_list[i][0])-float(final_list[i+1][0]))
            delta_first_j = np.abs(float(final_list[i][1])-float(final_list[i+1][1])) 
        
        f_funda       = delta_funda_j/radial_funda_unc
        f_first       = delta_first_j/radial_first_unc

        alpha                = 1#4.6
        chi_funda_pump       = (fund - radial_funda)**2/(radial_funda_unc**2*f_funda)
        chi_first_pump       = (first - radial_first)**2/(radial_first_unc**2*f_first)
        chi_allfreqs_pump    = 1/alpha*(chi_funda_pump + chi_first_pump)
        chi_funda            = ((fund-radial_funda)/radial_funda_unc)**2
        chi_first            = ((first-radial_first)/radial_first_unc)**2
        chi_allfreqs         = 1/alpha* (chi_funda + chi_first) 
        chi_teff             = ((teff-Log_Teff_obs)/Log_Teff_obs_unc)**2
        chi_g                = ((g-Log_g_obs)/Log_g_obs_unc)**2
        chi_l                = ((l-Log_L_obs)/Log_L_obs_unc)**2
        
        
        chi_rest   = (chi_teff + chi_g + chi_l)
        restfreqs  = chi_rest/chi_allfreqs
        
        
        ##### SECOND METHOD! #########################################################
        
#        # I = total number of different frequencies (=2 for l=0)
#        I = 2
#        sigma_j    = 1/I*np.sqrt((radial_funda-radial_funda_unc)**2+(radial_first-radial_first_unc)**2)
#        chi_allfreqs_m2 = (radial_funda-radial_funda_unc/sigma_j)**2+(radial_first-radial_first_unc/sigma_j)**2
        
        freqs_info += [[restfreqs, chi_rest, chi_allfreqs, chi_allfreqs_pump, f_funda, f_first]]
    
    
#        #chi        = (chi_rest + chi_allfreqs) 
        
#        #diff       = np.abs(chi_rest-chi_allfreqs)
        
        
#        likelihood = math.exp(0.5*(-chi**2)) #* age1  #if problems, consider log(weights) NOT Log10
#        loglikely = np.log(age1) - 0.5*chi**2

 #       N = 5#len(final_list)
 #       P = 0#5
 #       K = N-P
 #       red_chi   = chi/K
 #       total_chi += [[chi, red_chi, loglikely]]
 #       minimum = min(total_chi)
    
    freqs_forchi  = np.asarray(freqs_info)
    
    add_list = np.asarray(freqs_forchi[:,0])
    rest_list = np.asarray(freqs_forchi[:,1])
    allfreqs_list = np.asarray(freqs_forchi[:,2])
    allfreqs_pumped_list = np.asarray(freqs_forchi[:,3])
    funct_fundas  = np.asarray(freqs_forchi[:,4])
    funct_firsts  = np.asarray(freqs_forchi[:,5])
#    freqs_m2      = np.asarray(freqs_forchi[:,6])
    
    add_factor = np.sum(add_list)/len(add_list)
    print(add_factor)    
    #new_chi_freqs = allfreqs_list      #*add_factor. This add factor is in case we wish to weigh the frequencies by the ratio. 
    
    chi_final_pumped = allfreqs_pumped_list + rest_list
    chi_final        = allfreqs_list + rest_list
    
    #print(ages.index(maxagestep))
    output_chi = np.column_stack((funct_fundas, funct_firsts, allfreqs_list, allfreqs_pumped_list, chi_final, chi_final_pumped, rest_list))
    output_final = np.column_stack((final_list, output_chi))
    np.savetxt(result_name, output_final, delimiter=",", newline = "\n", fmt="%s")
    
    return output_final

for root, dirs, files in sorted(os.walk('/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid/Results_l0')):

    for file in files:
        if file.startswith('final_'):
            dirs = os.path.join(root,file)
            print(dirs)
            maindir = '/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid/new_Results_l0/'
            output_filename = maindir + '/' + os.path.join(file)
            output_final = getchis(dirs,output_filename)
                
