cd to middleware then run $ python gen_code_gen.py

This code will generate the following:

1. Synthesize a controller by running /tulip/controller.py and moving the generated file demo_controller.py to /auto_generated
2. Generate /auto_generated/auto_code.py
3. Generate /auto_generated/auto_code.xml

Then run AMASE and load the scenario file auto_code.xml and run script auto_code.py then hit play.

Note: At this stage the behaviors and monitors are not auto generated. the user must define the monitors and reactions to behaviors in the functions sense_something() and do_something() respectively in auto_code.py. An example is already there and commented out for sensing low fuel and the refuel contingency behavior.
