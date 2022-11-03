flag_on_windows=False

# the directory where all contracts are stored
contract_path='/media/sf___share_vms/sGuard_contracts/'  # on Virtual machine
if flag_on_windows:
    contract_path='C:\\Users\\18178\\_2022_exp\\sGuard_contracts\\' # on Windows

 


# the csv file that list all the contracts that will be evaulated
contract_data_csv='sGuard_contracts_info.csv'

# the directory that have the data for exp_general
dest_exp_general_path='/media/sf___share_vms/2022_exp_data_preparation/exp_mythril_smartExecutor/'


base_path_dict={
    "exp_phase2_3600s_1st":'C:\\22_summer_exp\\exp_phase2\\results_3600s\\1st\\',
    "exp_phase2_3600s_2nd":'C:\\22_summer_exp\\exp_phase2\\results_3600s\\2nd\\',
    "exp_phase2_3600s_3rd":'C:\\22_summer_exp\\exp_phase2\\results_3600s\\3rd\\',  
    }

