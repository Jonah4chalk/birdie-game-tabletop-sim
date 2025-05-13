.PHONY: install run clean

VENV_DIR = .venv

install: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/pip install -r requirements.txt
	
$(VENV_DIR)/bin/activate:
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install --upgrade pip

run:
	cd birdie-game && python3 manage.py runserver

clean:
	rm -rf $(VENV_DIR)