LEVEL := wwwhow

.PHONY: run

run:
	python3 run.py \
		--verbose debug

.PHONY: lint sort

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
		"$(LEVEL)"

sort:
	isort -cs -fss -m=5 -y -r "$(LEVEL)"


.PHONY: clean cleangit

define _gitclean
	git clean \
		-e "*.py" \
		-e "auth.json" \
		-e "logs/*.log" \
		$(1)
endef
clean:
	$(call _gitclean,-ndx)
cleangit:
	$(call _gitclean,-fdx)
