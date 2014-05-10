.PHONY: build_ext tests

build_ext: java
	python setup.py build_ext --inplace -g

install: java
	python setup.py install

java_src = $(wildcard jnius/java/org/jnius/*.java)
java: $(java_src:.java=.class)

html:
	$(MAKE) -C docs html

tests: build_ext
	cd tests && javac org/jnius/HelloWorld.java
	cd tests && javac org/jnius/BasicsTest.java
	cd tests && javac org/jnius/MultipleMethods.java
	cd tests && javac org/jnius/SimpleEnum.java
	cd tests && javac org/jnius/InterfaceWithPublicEnum.java
	cd tests && javac org/jnius/ClassArgument.java
	cd tests && javac org/jnius/MultipleDimensions.java
	cd tests && env PYTHONPATH=..:$(PYTHONPATH) CLASSPATH=".:../jnius/src" nosetests-2.7 -v

%.class: %.java
	javac $<
