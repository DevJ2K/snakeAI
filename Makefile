########################################
########## VARIABLES
FILES_DIR = main.py game.py srcs tests srcs/utils srcs/window

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

all: test

norm:
		@echo "$(CYAN)########################################"
		@echo "$(CYAN)######## NORM - Flake8 $(DEF_COLOR)"
		@python3 -m flake8 $(FILES_DIR) && echo "$(GREEN)SUCCESS $(DEF_COLOR)" || echo "$(RED)FAILURE $(DEF_COLOR)"

pytest:
		@echo "$(GREEN)########################################"
		@echo "$(GREEN)######## PYTEST $(DEF_COLOR)"
		@python3 -m pytest tests/*.py -v && echo "$(GREEN)SUCCESS $(DEF_COLOR)" || echo "$(RED)FAILURE $(DEF_COLOR)"

test: norm pytest

clean:
		rm -rf __pycache__ tests/__pycache__ srcs/__pycache__ .pytest_cache srcs/utils/__pycache__ srcs/window/__pycache__


.PHONY: all norm pytest test clean
