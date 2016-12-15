from scenario import Scenario


def dump(xs):
    for x in xs:
        print(x)


# TODO: maybe switch the specification format to JSON?
# TODO: take input argument from command line?
spec = Scenario.parse('spec.txt')

# determine which monitors will be required by the scenario
dump(spec.plays())
behaviors, monitors = spec.dependencies()
dump(behaviors)
dump(monitors)

# Write out the XML for AMASE
with open('../auto_generated/auto_code.xml', 'w') as xml:
    spec.gen_xml().writexml(xml, '', '  ', '\n')

# Write out the outer loop controller for the scenario
# with open('../auto_generated/auto_code.py', 'w') as script:
#     spec.gen_script(script)
with open('../auto_generated/auto_code.py', 'w') as script:
    spec.gen_script(script)

with open('../Java/PlayGUI.java', 'w') as script:
    spec.gen_GUI_script(script)