.PHONY: build_ext test java html clean install

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

clean:
	rm -f tests/org/jnius/*.class
	rm -f jnius/java/org/jnius/*.class
	rm -f jnius/jnius.{c,so,dll,dylib}
	rm -rf jnius.egg-info
	rm -rf build/ dist/

%.class: %.java
	javac $<
