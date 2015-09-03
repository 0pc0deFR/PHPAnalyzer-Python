from phpanalyzer import *
analyzer = Analyze('PHP_SOURCE_CODE_FILE')
print analyzer
analyzer.classes()
analyzer.construct_class("CLASS")
analyzer.functions()
analyzer.params_functions("FUNCTION")
analyzer.defines()
analyzer.compile()