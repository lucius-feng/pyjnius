import inspect, os
import jnius_config

thisfile = inspect.getfile(inspect.currentframe())
testdir = os.path.dirname(os.path.abspath(thisfile))
jnius_config.add_classpath(testdir)
