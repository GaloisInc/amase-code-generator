
SALTY ?= $(shell find ../../.. -name salty -type f | head -n1)
SLUGS ?= $(shell find ../../../ -name slugs -type f)

ifeq ("$(SALTY)","")
	$(error Unable to find salty)
endif

ifeq ("$(SLUGS)", "")
	$(error Unable to find slugs)
endif

../auto_generated/demo_controller.py: DemoController.py
	mv $< $@

DemoController.py: controller.salt
	$(SALTY) -s $(SLUGS) -p $<

.PHONY: clean
clean:
	$(RM) DemoController.py

print-%:
	@echo "$* = $($*)"

gen-%:
	$(SALTY) -s $(SLUGS) -p $*
