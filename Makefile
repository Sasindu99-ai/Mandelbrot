# Makefile

# Define a variable for the poetry command to keep it DRY
POETRY = poetry
RUN = python3 main.py

# Load poetry
.PHONY: load
load:
	export PATH='$$HOME/.local/bin:$$PATH'

# Install dependencies
.PHONY: install
install:
	$(POETRY) install

# Install pre-commit hooks
.PHONE: install-pre-commit
install-pre-commit:
	$(POETRY) run pre-commit uninstall
	$(POETRY) run pre-commit install

# Check code style
.PHONY: lint
lint:
	$(POETRY) run pre-commit run --all-files

# Update project dependencies
.PHONY: update
update: install;

# Run the game
.PHONY: run
run:
	$(POETRY) run $(RUN)
