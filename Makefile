########################################
########## VARIABLES
DIRECTORY = srcs utils tests

########################################
########## COLORS
DEF_COLOR = \033[0;39m
GRAY = \033[1;90m
RED = \033[1;91m
GREEN = \033[1;92m
YELLOW = \033[1;93m
BLUE = \033[1;94m
MAGENTA = \033[1;95m
CYAN = \033[1;96m
WHITE = \033[1;97m

########################################
########## RULES

all:
		python3 main.py
		echo ALL

norm:
		@echo "$(CYAN)########################################"
		@echo "$(CYAN)######## NORM - Flake8 $(DEF_COLOR)"
		@python3 -m flake8 $(DIRECTORY)

path:
# export PATH=$$PWD:$$PATH
		chmod +x script.sh && ./script.sh
# export PATH=$$PWD

pytest:
		@echo "$(GREEN)########################################"
		@echo "$(GREEN)######## PYTEST $(DEF_COLOR)"
		@python3 -m pytest tests/*.py -v

clean:
		rm -rf __pycache__ tests/__pycache__ srcs/__pycache__ .pytest_cache

test: norm pytest

.PHONY: all norm pytest test clean
