import sys
from scenario import Scenario

# TODO: maybe switch the specification format to JSON?
spec = Scenario.parse('spec.txt')

for play in spec.plays():
    print str(play)

# determine which monitors will be required by the scenario
behaviors, monitors = spec.dependencies()
for behavior in behaviors:
    print str(behavior)
for monitor in monitors:
    print str(monitor)

# Write out the XML for AMASE
with open('../auto_generated/auto_code.xml', 'w') as xml:
    spec.gen_xml().writexml(xml, '', '  ', '\n')

# Write out the outer loop controller for the scenario
# with open('../auto_generated/auto_code.py', 'w') as script:
#     spec.gen_script(script)
with open('../auto_generated/auto_code.py', 'w') as script:
    spec.gen_script(script)
