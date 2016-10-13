
EXTRA ?=

SALTY ?=
SLUGS ?=

ifeq ("$(SALTY)","")
	$(error Unable to find salty)
endif

ifeq ("$(SLUGS)", "")
	$(error Unable to find slugs)
endif

../auto_generated/demo_controller.py: ExampleCtrl.py
	mv $< $@

ExampleCtrl.py: controller.salt
	$(SALTY) $(EXTRA) -s $(SLUGS) -p $<

.PHONY: clean
clean:
	$(RM) ExampleCtrl.py

print-%:
	@echo "$* = $($*)"

gen-%:
	$(SALTY) -s $(SLUGS) -p $*
