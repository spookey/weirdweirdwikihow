WWWHOW := wwwhow
TWFOLL := twfoll


.PHONY: help

help:
	@echo "[wh]"	"\t~>\t"	"WikiHow"
	@echo "[tw]"	"\t~>\t"	"Twitter Follow"
	@echo
	@echo "linttw"		"\t\t"	"lint $(TWFOLL)"
	@echo "lintwh"		"\t\t"	"lint $(WWWHOW)"
	@echo "sorttw"		"\t\t"	"sort $(TWFOLL)"
	@echo "sortwh"		"\t\t"	"sort $(WWWHOW)"
	@echo
	@echo "clean"		"\t\t"	"show cleanup files"
	@echo "cleangit"	"\t"	"do git cleanup"


.PHONY: lintwh linttw

define PYLINT_MESSAGE_TEMPLATE
{C} {path}:{line}:{column} - {msg}
	↪  {category} {module}.{obj} ({symbol} {msg_id})
endef
export PYLINT_MESSAGE_TEMPLATE

define _pylint
	pylint \
		--disable "C0111" `#missing docstring` \
		--disable "RP0401" `#external dependencies` \
		--msg-template="$$PYLINT_MESSAGE_TEMPLATE" \
		--output-format="colorized" \
			$(1)
endef

lintwh:
	$(call _pylint,"$(WWWHOW)")
linttw:
	$(call _pylint,"$(TWFOLL)")


.PHONY:  sortwh sorttw

define _sort
	isort -cs -fss -m=5 -y -rc $(1)
endef

sortwh:
	$(call _sort,"$(WWWHOW)")
sorttw:
	$(call _sort,"$(TWFOLL)")


.PHONY: clean cleangit

define _gitclean
	git clean \
		-e "*.py" \
		-e "*.json" \
		-e "logs/" \
		-e "venv/" \
		$(1)
endef

clean:
	$(call _gitclean,-ndx)
cleangit:
	$(call _gitclean,-fdx)
