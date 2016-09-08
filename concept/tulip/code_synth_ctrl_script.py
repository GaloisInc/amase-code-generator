from tulip import spec, synth, transys
from tulip import dumpsmach
import cPickle as pickle
import time
start_time = time.time()

env_init = set()
sys_init = set()
env_prog = set()
sys_prog = set()
env_safe = set()
sys_safe = set()

env_vars = {'P_1_Loiter_0_0': (0, 1), 'P_2_Loiter_0_0': (0, 1), 'P_1_ST_2_A': (0, 1)\
           , 'P_1_ST_2_B': (0,1), 'P_1_PU_0_A': (0, 1), 'P_1_PU_0_B': (0, 1)}

sys_vars = {'M_1_Fuel_0_0': (0, 1), 'M_2_Fuel_0_0': (0, 1), 'M_1_Found_2_0': (0, 1)\
           , 'M_1_Data_0_0': (0, 1), 'B_1_Refuel_0_0': (0, 1), 'B_2_Refuel_0_0': (0, 1)\
           , 'B_1_Search_0_0': (0, 1), 'B_1_Search_0_1': (0, 1), 'B_1_Upload_0_0': (0, 1)\
           ,'B_1_Track_2_0': (0, 1), 'B_1_Loiter_0_0': (0, 1), 'B_2_Loiter_0_0': (0, 1)}

sys_safe |= {(' P_1_Loiter_0_0 = 1 -> B_1_Loiter_0_0 = 1 && B_1_Refuel_0_0 = 1'+
' && M_1_Fuel_0_0 = 1 ')}
sys_safe |= {(' P_2_Loiter_0_0 = 1 -> B_2_Loiter_0_0 = 1 && B_2_Refuel_0_0 = 1'+
' && M_2_Fuel_0_0 = 1 ')}

sys_safe |= {(' P_1_Loiter_0_0 = 0 -> B_1_Loiter_0_0 = 0')}
sys_safe |= {(' P_2_Loiter_0_0 = 0 -> B_2_Loiter_0_0 = 0')}

sys_safe |= {(' P_1_ST_2_A = 1 -> B_1_Search_0_0 = 1 && B_1_Track_2_0 = 1 &&'+
	' B_1_Refuel_0_0 = 1 && M_1_Fuel_0_0 = 1 && M_1_Found_2_0 = 1 ')}
sys_safe |= {(' P_1_ST_2_B = 1 -> B_1_Search_0_1 = 1 && B_1_Track_2_0 = 1 &&'+
	' B_1_Refuel_0_0 = 1 && M_1_Fuel_0_0 = 1 && M_1_Found_2_0 = 1 ')}

sys_safe |= {(' P_1_ST_2_A = 0 && P_1_PU_0_A = 0 -> B_1_Search_0_0 = 0')}
sys_safe |= {(' P_1_ST_2_B = 0 && P_1_PU_0_B = 0 -> B_1_Search_0_1 = 0')}

sys_safe |= {(' P_1_ST_2_A = 0 && P_1_ST_2_B = 0 -> B_1_Track_2_0 = 0')}

sys_safe |= {(' P_1_PU_0_B = 0 && P_1_PU_0_A = 0 -> B_1_Upload_0_0 = 0')}

sys_safe |= {(' P_1_PU_0_A = 1 -> B_1_Search_0_0 = 1 && B_1_Upload_0_0 = 1 &&'+
	' M_1_Fuel_0_0 = 1 && M_1_Data_0_0 = 1 ')}
sys_safe |= {(' P_1_PU_0_B = 1 -> B_1_Search_0_1 = 1 && B_1_Upload_0_0 = 1 &&'+
	' M_1_Fuel_0_0 = 1 && M_1_Data_0_0 = 1 ')}

specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init, env_safe, sys_safe,\
 env_prog, sys_prog)

ctrl = synth.synthesize('gr1c', specs)

print("Synthesis: --- %s seconds ---" % (time.time() - start_time))

start_time = time.time()

dumpsmach.write_python_case("code_synth_ctrl.py", ctrl, classname="CodeSynthCtrl")

print specs.pretty()
print("Code Gen: --- %s seconds ---" % (time.time() - start_time))