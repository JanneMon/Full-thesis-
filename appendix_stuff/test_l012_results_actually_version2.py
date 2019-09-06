import os
import numpy as np

dire = '/usr/users/jhm1496/stars/44_tau/44_tau/output_smallgrid/Results_l012'

for root, dirs, files in sorted(os.walk(dire)):
    files.sort(key=lambda x: '{0:0>20}'.format(x))
    for file in files:
        if file.startswith('final_fivep.txt'):
            finals = []
            directory = os.path.join(root,file)
            filename = directory
            final_list = []
            with open(filename) as f:
               for line in f:
                  inner_list = [elt.strip() for elt in line.split(',')]
                  final_list.append(inner_list)
            #print(final_list)
            finals += [final_list]
            #for i in range(0,len(finals)):
            #   chi2_freqs = final_list[i][9]

            final = np.concatenate(finals)
            #print(np.shape(final))
            chi2_params = final[:,2].astype('float')
            chi2_freqs = final[:,3].astype('float')
            chi2_freqs_pumped = final[:,4].astype('float')
            chi2_tot = final[:,5]
            chi2_tot_pumped = final[:,6]

#            print(chi2_tot[0], chi2_tot_pumped[0])
            #print(chi2_param)
            minimum_freqs = min(chi2_freqs.astype('float'))
            minimum_freqs_pumped = min(chi2_freqs_pumped.astype('float'))
            minimum_chi_tot = min(chi2_tot.astype('float'))
            minimum_chi_tot_pumped = min(chi2_tot_pumped.astype('float'))
            minimum_param = min(chi2_params.astype('float'))
            print(minimum_chi_tot_pumped)

            index_minfreqs = np.where(chi2_freqs.astype('float') == minimum_freqs)
            index_minfreqs_pumped = np.where(chi2_freqs_pumped.astype('float') == minimum_freqs_pumped)
            index_minchi = np.where(chi2_tot.astype('float') == minimum_chi_tot)
            index_minchi_pumped = np.where(chi2_tot_pumped.astype('float') == minimum_chi_tot_pumped)
            index_minparam = np.where(chi2_params.astype('float') == minimum_param)
          
#print(chi2_tot, minimum_chi_tot)
print(final[index_minchi,:], minimum_chi_tot)
print(final[index_minfreqs,:], minimum_freqs)
print(final[index_minparam,:], minimum_param)
print(final[index_minchi_pumped,:], minimum_chi_tot_pumped)
