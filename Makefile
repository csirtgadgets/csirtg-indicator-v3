.PHONY: clean test sdist all test

all: test sdist

clean:
	rm -rf `find . | grep \.pyc`
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

test:
	@python setup.py test 

dist: sdist

sdist:
	@python setup.py sdist
