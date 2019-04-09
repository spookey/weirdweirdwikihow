WWWHOW := wwwhow
TWFOLL := twfoll
SHARED := shared


.PHONY: help

help:
	@echo "lint"		"\t\t"	"lint code"
	@echo "sort"		"\t\t"	"sort imports"
	@echo "clean"		"\t\t"	"show cleanup files"
	@echo "cleangit"	"\t"	"do git cleanup"


.PHONY: lint

define PYLINT_MESSAGE_TEMPLATE
{C} {path}:{line}:{column} - {msg}
  ↪  {category} {module}.{obj} ({symbol} {msg_id})
endef
export PYLINT_MESSAGE_TEMPLATE

lint:
	pylint \
		--disable "C0111" `#missing docstring` \
		--disable "RP0401" `#external dependencies` \
		--msg-template="$$PYLINT_MESSAGE_TEMPLATE" \
		--output-format="colorized" \
			"$(WWWHOW)" "$(TWFOLL)" "$(SHARED)"


.PHONY: sort

sort:
	isort -cs -fss -m=5 -y -rc "$(WWWHOW)" "$(TWFOLL)" "$(SHARED)"


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
