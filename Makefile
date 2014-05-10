.PHONY: build_ext tests

build_ext: java
	python setup.py build_ext --inplace -g

install: java
	python setup.py install

java_src = $(wildcard jnius/java/org/jnius/*.java)
java: $(java_src:.java=.class)

html:
	$(MAKE) -C docs html

java_test_src = $(wildcard tests/org/jnius/*.java)

test: build_ext $(java_test_src:.java=.class)
	python setup.py test

%.class: %.java
	javac $<
