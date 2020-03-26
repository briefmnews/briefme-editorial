clean:
	rm -rf *.egg-info .pytest_cache
	rm -rf htmlcov
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

coverage:
	pytest --cov=briefme_editorial tests

report:
	pytest --cov=briefme_editorial --cov-report=html tests

install:
	pip install -r test_requirements.txt
