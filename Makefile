upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*

test:
	tox
