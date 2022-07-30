VENV=makefile_venv

virtual_env:
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate

all:
	@echo " -\n -\n -\n O codigo está na pasta target criada aqui: \n 	./src/lexer.py \n Para executar basta rodar:\n		python src/lexer.py \n"
src/lexer.py: lexer
lexer:
	setup
run:
	python lexer.py
setup:
	if ! dpkg -l | grep python3-venv -c >>/dev/null; then sudo apt-get update && sudo apt-get install python3-venv; fi
	make virtual_env
	python3 -m pip install --user --upgrade pip
	python3 -m pip install --user -r requirements.txt
	@make env_activate
clean :
	rm -rf __pychache__
	rm -rf makefile_venv
	@echo ">>>>>>>>>>>>>>> Virtual environment deleted <<<<<<<<<<<<<<<"

env_activate:
	@echo ">>>>>>>>>>>>>>> Make sure to activate virtual environment again <<<<<<<<<<<<<<<"