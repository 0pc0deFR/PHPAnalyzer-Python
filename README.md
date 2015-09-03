#PHPAnalyzer

PHPAnalyzer is python library used for analyze PHP source code. This library will be used for the next version of WordPress Auditor.  

WARNING: This library is in development version. It is used in the state but many bugs may be found.  

##Use
The library is constituted in two classes. The first class is the Loader, used for load the source code. The second class is the Analyzer, used for analyze the source code.  

###Example of use
```
import phpanalyzer from *

analyzer = Analyze('PHP Source Code File')
```
The example return an instance.  
This instance provides access to several functions:  
	- classes(): return all classes founded in file, in list  
	- construct_class(Class): return the method and the parameters if construct is found in Class, in dictonary  
	- functions(): return all functions found in file, in list  
	- params_functions(Function): return the parameters of Function, in dictionary  
	- defines(): return all defines found in file, in dictionary  
	- compile(): execute all functions and return three dictionary with all informations returned by all functions  
