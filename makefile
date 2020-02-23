WWWHOW		:=	wwwhow
TWFOLL		:=	twfoll
SHARED		:=	shared

CMD_GIT		:=	git
CMD_VENV	:=	virtualenv
DIR_VENV	:=	venv
VER_PY		:=	3.7

DIR_BIN		:=	$(DIR_VENV)/bin
DIR_SITE	:=	$(DIR_VENV)/lib/python$(VER_PY)/site-packages

CMD_PIP		:=	$(DIR_BIN)/pip$(VER_PY)
CMD_PY		:=	$(DIR_BIN)/python$(VER_PY)
CMD_PYLINT	:=	$(DIR_BIN)/pylint
CMD_ISORT	:=	$(DIR_BIN)/isort

LIB_BS4		:=	$(DIR_SITE)/bs4/__init__.py
LIB_REQ		:=	$(DIR_SITE)/requests/__init__.py
LIB_TWE		:=	$(DIR_SITE)/tweepy/__init__.py


.PHONY: help

help:
	@echo "venv                  install virtualenv"
	@echo "requirements          install requirements into venv"
	@echo
	@echo "lint                  lint code"
	@echo "sort                  sort imports"
	@echo "clean                 show cleanup files"
	@echo "cleanup               do git cleanup"


$(DIR_VENV):
	$(CMD_VENV) -p "python$(VER_PY)" "$(DIR_VENV)"

.PHONY: requirements
requirements: $(LIB_BS4) $(LIB_REQ) $(LIB_TWE)

$(LIB_BS4) $(LIB_REQ) $(LIB_TWE): $(DIR_VENV)
	$(CMD_PIP) install -r "requirements.txt"


.PHONY: lint

define PYLINT_MESSAGE_TEMPLATE
{C} {path}:{line}:{column} - {msg}
  ↪  {category} {module}.{obj} ({symbol} {msg_id})
endef
export PYLINT_MESSAGE_TEMPLATE

lint:
	$(CMD_PYLINT) \
		--disable "C0111" \
		--msg-template="$$PYLINT_MESSAGE_TEMPLATE" \
		--output-format="colorized" \
			"$(WWWHOW)" "$(TWFOLL)" "$(SHARED)"


.PHONY: sort

sort:
	$(CMD_ISORT) -cs -fss -m=5 -y -rc "$(WWWHOW)" "$(TWFOLL)" "$(SHARED)"


.PHONY: clean cleanup

define _gitclean
	$(CMD_GIT) clean \
		-e "*.py" \
		-e "*.json" \
		-e "logs/" \
		-e "venv/" \
		$(1)
endef

clean:
	$(call _gitclean,-ndx)
cleanup:
	$(call _gitclean,-fdx)
