.PHONY: validate lint test test-release release-audit release-plan

validate:
	python3 scripts/validate_skills.py
	python3 scripts/release.py validate
	python3 scripts/build_chatgpt_smoke_bundle.py

lint:
	ruff check scripts tests

test:
	python3 -m unittest discover -s tests

test-release:
	python3 -m unittest tests.test_release tests.test_release_workflow

release-audit:
	python3 scripts/release.py audit

release-plan:
	python3 scripts/release.py plan
