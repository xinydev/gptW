.PHONY: test
test:
	@tox

.PHONY: install
install:
	@pip3 install .

.PHONY: lint
lint:
	@pre-commit run --show-diff-on-failure -a
