
python_deps := $(wildcard *.py)

.PHONY: all
all: ../auto_generated/demo_controller.py ../auto_generated/auto_code.py \
       	../auto_generated/auto_code.xml

.PHONY: clean
clean:
	$(RM) ../auto_generated/auto_code.py
	$(RM) ../auto_generated/auto_code.xml

.PHONY: test
test: clean ../auto_generated/auto_code.py
	( cd ../auto_generated && python auto_code.py )

.PHONY: run
run: all
	( cd ../auto_generated && python auto_code.py )

../auto_generated/auto_code.xml: ../auto_generated/auto_code.py ;

../auto_generated/auto_code.py: spec.txt $(python_deps)
	python xml_client_code_gen.py

../auto_generated/demo_controller.py: ../salty/controller.salt
	$(MAKE) -C ../salty
