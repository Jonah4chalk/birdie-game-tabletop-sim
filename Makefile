.PHONY: install run clean

VENV_DIR = venv

install: $(VENV_DIR)/Source/activate
	$(VENV_DIR)/Source/pip install -r requirements.txt
	
$(VENV_DIR)/Source/activate:
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/Source/pip install --upgrade pip

run:
	cd birdie-game && python3 manage.py runserver

clean:
	rm -rf $(VENV_DIR)