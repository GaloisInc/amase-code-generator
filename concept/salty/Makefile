
SALTY ?= $(shell find ../../.. -name salty -type f | head -n1)
SLUGS ?= $(shell find ../../../ -name slugs -type f)

ifeq ("$(SALTY)","")
	$(error Unable to find salty)
endif

ifeq ("$(SLUGS)", "")
	$(error Unable to find slugs)
endif

code_synth_ctrl.py: CodeSynthCtrl.py
	mv $< $@

CodeSynthCtrl.py: controller.salt
	$(SALTY) -s $(SLUGS) -p $<

.PHONY: clean
clean:
	$(RM) code_synth_ctrl.py CodeSynthCtrl.py

print-%:
	@echo "$* = $($*)"

gen-%:
	$(SALTY) -s $(SLUGS) -p $*
