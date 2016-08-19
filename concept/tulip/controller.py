from tulip import spec, synth, transys
import cPickle as pickle
import time
from tulip import dumpsmach

start = time.clock()

env_vars = dict()
sys_vars = dict()

env_init = set()
sys_init = set()
env_safe = set()
sys_safe = set()
env_prog = set()
sys_prog = set()

env_vars['Monitor_lowFuel'] = (0,1)
env_vars['Monitor_target'] = (0,1)
env_vars['Monitor_data'] = (0,1)

env_vars['Play_trackTarget'] = (0,1)
env_vars['Play_searchForest'] = (0,1)

sys_vars['B_search'] = (0,1)
sys_vars['B_track'] = (0,1)
sys_vars['B_deliver'] = (0,1)
sys_vars['B_refuel'] = (0,1)

env_safe |= {'(Play_trackTarget = 1) -> (Play_searchForest = 0)'}

env_safe |= {'(Play_searchForest = 1) -> (Play_trackTarget = 0)'}

sys_safe |= {'( (Play_trackTarget = 1) && (Monitor_lowFuel = 0) && (Monitor_target = 0)) -> (B_search = 1)'}

sys_safe |= {'(B_search = 1) ->  ((Play_trackTarget = 1) || (Play_searchForest = 1))'}

sys_safe |= {'( (Play_trackTarget = 1) && (Monitor_lowFuel = 0) && (Monitor_target = 1)) -> (B_track = 1)'}

sys_safe |= {'( (B_track = 1)) -> (Play_trackTarget = 1)'}

sys_safe |= {'((Monitor_lowFuel = 1)) -> (B_refuel = 1)'}

sys_safe |= {'((B_refuel = 1)) -> (Monitor_lowFuel = 1)'}

sys_safe |= {'( (Play_searchForest = 1) && (Monitor_lowFuel = 0) && (Monitor_data = 0)) -> (B_search = 1)'}

sys_safe |= {'((B_search = 1)) -> ((B_refuel = 0) && (B_track = 0)&&(B_deliver = 0))'}

sys_safe |= {'((B_refuel = 1)) -> ((B_search = 0) && (B_track = 0)&&(B_deliver = 0))'}

sys_safe |= {'((B_track = 1)) -> ((B_refuel = 0) && (B_search = 0)&&(B_deliver = 0))'}

sys_safe |= {'((B_deliver = 1)) -> ((B_refuel = 0) && (B_search = 0)&&(B_track = 0))'}

specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                    env_safe, sys_safe, env_prog, sys_prog)

ctrl = synth.synthesize('gr1c',specs)
finish = time.clock()
print finish - start
dumpsmach.write_python_case("demo_controller.py", ctrl, classname="ExampleCtrl")
finish = time.clock()
print finish - start
print specs.pretty()