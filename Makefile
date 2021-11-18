.PHONY: clean-pyc run-test run-sample help

TOP_DIR=.
TESTS_DIR=tests

help:
	@echo "make clean-pyc"
	@echo "    Remove python artifacts."
	@echo ""
	@echo "make run-test"
	@echo "    Run all test scripts."
	@echo ""
	@echo "make run-sample"
	@echo "    Run sample implementation of cascading autonomous agents."

clean-pyc:
	@find $(TOP_DIR) -name '*.pyc' -exec rm -rvf {} +
	@find $(TOP_DIR) -name '*.pyo' -exec rm -rvf {} +
	@find $(TOP_DIR) -name '__pycache*' -exec rm -rvf {} +
	@find $(TESTS_DIR)/ -name '__pycache*' -exec rm -rvf {} +

run-flake8: clean-pyc
	sh $(TOP_DIR)/run_flake8.sh

run-test: clean-pyc
	PYTHONPATH=$(TOP_DIR):$(PYTHONPATH) python3 -m unittest $(TESTS_DIR)/*

run-sample: clean-pyc
	PYTHONPATH=$(TOP_DIR):$(PYTHONPATH) python3 autonomous_agent.py
