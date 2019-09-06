
"""
Created on Wed Apr 10 11:25:35 2019

@author: janne
"""
import gyre_output_read as gar
import numpy as np
import mesa_reader as mr
import os

Log_L_obs = 1.305
Log_Teff_obs = 3.839
Log_g_obs = 3.6
Log_Teff_obs_unc = 0.007
Log_L_obs_unc = 0.065 
Log_g_obs_unc = 0.1

final_list = []
#files_tofindchi = []
mean_functs = []
kolonner_m1 = []
kolonner_m2 = []
alphas = []
chis_final_pumped = []
chis_final = []
chis_rests = []
chis_freqs_pumped = []
chis_freqs = []
#final_list2 = []   
    
filename = '/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid/new_Results_l0/bestfivep.txt' #lum1 m1
with open(filename) as f:
    for line in f:
        inner_list = [elt.strip() for elt in line.split(',')]
        final_list.append(inner_list)
#print(final_list)
array = np.asarray(final_list)
logfiles = array[:,0]
profile = array[:,1]
print(logfiles, profile)
for k in range(0,len(logfiles)):
    final_list2 = []
    logdir = logfiles[k].lstrip('final_')
    logdir2 = logdir.rstrip('.txt')
    pnum1 = profile[k].lstrip('profile')
    pnum2 = pnum1.rstrip('.data')
    logs_profiledir = logdir2 + '/' + profile[k]
    maindir = '/usr/users/jhm1496/stars/python_scripts/bestfive_dirs'
    direc = maindir + '/' + logdir2 + '/profile' + pnum2 + '-freqs.dat' # Directory with l=1 and l=2 modes
    print(direc)
    
#    final_list2 = []
    finalarray = []
    bm_array2 = []
    #dires = os.path.join(root,file)
    data = gar.readmesa(direc)
    harm_degree = data['l']          
    radial_order= data['n_pg']

    re_freq_theo = data['Refreq'] # these are the frequencies that will be compared to Lenz and observations. 
    #im_freq = data['Imfreq'] #imaginary part of frequencies are not observable. 
    #print(re_freq_theo)

    re_freq_obs = [ 6.8980209, 7.00599425, 9.11743254, 11.5196319, 8.96062045, 8.96062045, 7.30312483, 6.7954641, 9.58283134, 6.33900993, 8.63914838, 11.2947181]
   # re_freq_obs_unc     = listofzeros = [10**(-7)] * len(re_freq_obs)#np.ones(len(re_freq_obs))*10**(-7)
    re_freq_obs_unc = [7.432077540*10**(-7), 2.010925863*10**(-6), 2.363621297*10**(-6), 1.999560327*10**(-6), 2.243216851*10**(-6), 3.090801973*10**(-6), 4.622296759*10**(-6), 8.973641778*10**(-6), 1.712537114*10**(-5), 1.400802170*10**(-5), 1.331246928*10**(-5), 2.178014501*10**(-5) ]
    #print(len(np.atleast_1d(re_freq_theo)))
    #re_freq_obs_unc = np.ones(len(re_freq_obs)) * 0.1
    remaining_obs = re_freq_obs 
    remaining_obs_unc = re_freq_obs_unc
    remaining_theo = np.atleast_1d(re_freq_theo)
    remaining_ells = np.atleast_1d(harm_degree)
    remaining_radial = np.atleast_1d(radial_order)

    best_matching = []
    #names = []

    for ii in range(min(len(np.atleast_1d(re_freq_theo)), len(re_freq_obs))): #default: freq_obs, but depends if freq_obs is longer than re_freq
        best = np.inf
        bestjj = -1
        bestkk = -1

        #print(len(remaining_obs))

        for jj in range(len(np.atleast_1d(remaining_theo))):
            for kk in range(len(remaining_obs)):
                val = (remaining_theo[jj] - remaining_obs[kk])**2 / 4 #put uncertainty here  
                if (val < best):
                    best = val
                    bestjj = jj
                    bestkk = kk
                    
                    # print(best, bestjj, bestkk)
        best_matching += [[remaining_ells[bestjj], remaining_radial[bestjj], remaining_theo[bestjj], remaining_obs[bestkk], remaining_obs_unc[bestkk]]]
            
        remaining_theo = np.delete(remaining_theo, bestjj)
        remaining_ells = np.delete(remaining_ells, bestjj)
        remaining_obs = np.delete(remaining_obs, bestkk)
        remaining_obs_unc = np.delete(remaining_obs_unc, bestkk)
        remaining_radial = np.delete(remaining_radial,bestjj)

        #diff = np.asarray(diff)
        #final = np.append(bm_array,diff)

    bm_array = np.asarray(best_matching)           
    bm_array2 += [bm_array]
    finalarray += [[bm_array, pnum2]]
    print(finalarray)
    
    #### FIRST METHOD ############################################################################
#    final_list2 = []
    filename2 = '/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid/new_Results_l0/final_' + logdir2 + '.txt'
    with open(filename2) as f2:
        for line2 in f2:
            inner_list2 = [elt.strip() for elt in line2.split(',')]
            final_list2.append(inner_list2)
        
    for i in range(0,len(final_list2)):
        profilenumber = float(final_list2[i][7])
        #print(profilenumber, pnum2)
        if int(profilenumber) == int(float(pnum2)):
            teff        = float(final_list2[i][8])
            logg        = float(final_list2[i][9])
            logl        = float(final_list2[i][10])
            funct_funda = float(final_list2[i][15])
            funct_first = float(final_list2[i][16])
            mean = (funct_funda + funct_first)/2
            
            chi_teff  = ((teff-Log_Teff_obs)/Log_Teff_obs_unc)**2
            chi_g     = ((logg-Log_g_obs)/Log_g_obs_unc)**2
            chi_l     = ((logl-Log_L_obs)/Log_L_obs_unc)**2
            chi_rest  = chi_teff + chi_g + chi_l
            #chis_rests += [chi_rest]
            mean_functs += [mean]        
    
            chi2sum_pump = {}
            chi2sum = {}
            chi2sigma = {}
            chi2m2 = {}
            chiforalpha = {}
            chi2m1 = {}
            #print(finalarray)
            
            for ii in range(len(finalarray)):
                for kk in range(len(finalarray[ii][0])):
                    pname = finalarray[ii][1]
                    if pname not in chi2sum.keys():
                        chi2sum_pump[pname] = 0
                        chi2sum[pname] = 0
                        chi2sigma[pname] = 0
                        chi2m2[pname] = 0
                        
                    chi2sum_pump[pname] = (chi2sum[pname] + (finalarray[ii][0][kk][2] - finalarray[ii][0][kk][3])**2/(finalarray[ii][0][kk][4]**2 * mean))
                    chi2sum[pname] = (chi2sum[pname] + (finalarray[ii][0][kk][2] - finalarray[ii][0][kk][3])**2/(finalarray[ii][0][kk][4]**2))
                    chi2sigma[pname] = chi2sigma[pname] + (finalarray[ii][0][kk][2] - finalarray[ii][0][kk][3])**2

            # for ii in range(len(finalarray)):
            #     pname = finalarray[ii][1]
            #     sigma_value = 1/len(finalarray[ii][0])*np.sqrt(chi2sigma[pname])
                
            #     for kk in range(len(finalarray[ii][0])):
            #         chi2m2[pname] = chi2m2[pname] + ((finalarray[ii][0][kk][2] - finalarray[ii][0][kk][3])/sigma_value)**2 
            #         print(chi2m2,kk)
                    
            m1 = chi2sum_pump.values()
            m2 = chi2sum.values()
            
            #for g in m1:
            #    alpha_m1 = chi_rest/g
            #    alphas += [alpha_m1]
                    
            #    alphas_to = np.asarray(alphas)
            #    final_alpha = 1#np.sum(alphas_to)/len(alphas_to)

            final_alpha = 1

            for n in m1:
                 allfreqs_pumped = final_alpha * n
                 chi_m1 = allfreqs_pumped + chi_rest
                 chis_freqs_pumped += [allfreqs_pumped]
                 chis_final_pumped += [chi_m1] 
            for m in m2:
                 allfreqs = m
                 chi_m2 = m + chi_rest
                 chis_freqs += [allfreqs]
                 chis_final += [chi_m2]
                 chis_rests += [chi_rest]
            #chis_freqs += [allfreqs]
            #chis_freqs_pumped += [allfreqs_pumped]
            #chis_final_pumped += [chi_m1]
            #chis_final+= [chi_m2]
            #chis_rests += [chi_rest]                        
            #kolonner_m1 += [list(m1)]
            #kolonner_m2 += [list(m2)]

#print(len(final_list))
#print(len(chis_rests))
#print(len(chis_final))
#print(len(chis_final_pumped))
print(chis_final[0], chis_freqs[0], chis_rests[0])
   
output = np.column_stack((final_list, chis_rests, chis_freqs, chis_freqs_pumped, chis_final, chis_final_pumped))
savedir = '/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid/Results_l012/' + 'final_fivep.txt'
np.savetxt(savedir, output, delimiter=",", newline = "\n", fmt="%s")
 

#finalarray, kolonne = to_get_chi2('/home/janne/Gunter_project/44_tau/new_chi_method/Results/')
                
