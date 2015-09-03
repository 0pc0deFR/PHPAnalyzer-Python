import re
import os

class _Load:
	"""
	Load .php file
	"""
	def __init__(self, php_file):
		self._file = php_file


	def _CheckFile(self):
		if os.path.isfile(self._file):
			return True
		else:
			raise Exception, "%s isn't a readable file" % self._file
			return False

	def LoadFile(self):
		try:
			if self._CheckFile() == True:
				open_file = open(self._file, 'r')
				read = open_file.read()
				open_file.close()
			return read
		except IOError as e:
   			print "I/O error({0}): {1}".format(e.errno, e.strerror)
   			return False

class Analyze:
	"""
	Analyze .php file
	"""
	def __init__(self, name_file):
		loader =_Load(name_file)
		self._content_file = loader.LoadFile()
		self._name = ''
		self._destruct_comment()

	def _destruct_comment(self):
		regex = re.compile('(\\/)(\\*).*?(\\*)(\\/)',re.IGNORECASE|re.DOTALL)
		self._content_file = re.sub(regex, "", self._content_file)
		regex = re.compile('(\\/)(\\/).*?.\n', re.IGNORECASE|re.DOTALL)
		self._content_file = re.sub(regex, "", self._content_file)
		regex = re.compile('(#).*?.\n', re.IGNORECASE|re.DOTALL)
		self._content_file = re.sub(regex, "", self._content_file)

	def classes(self):
		tab = []
		regex = re.compile('(class)( )((?:[a-z][a-z0-9_]*))',re.IGNORECASE|re.DOTALL)
		m = regex.findall(self._content_file)
		for n in m:
			tab.append(n[2])
		return tab

	def construct_class(self, class_analyze):
		tab = {}
		tab["class"] = class_analyze
		start_class = self._content_file.find(class_analyze, 0)
		start_construct = self._content_file.find("__construct", start_class)
		end_construct = self._content_file.find(")", start_construct)
		if self._content_file[start_construct:end_construct].find("__construct(") != -1:
			tab["__construct"] = True
		else:
			tab["__construct"] = False
			return tab
		if self._content_file.find("private", start_class, start_construct) != -1:
			tab["method"] = "private"
		elif self._content_file.find("protected", start_class, start_construct) != -1:
			tab["method"] = "protected"
		else:
			tab["method"] = "public"
		params = self._content_file[start_construct+12:end_construct]
		params = params.split(",")
		i = 1
		for param in params:
			if param != '':
				tab["param" + str(i)] = param
			i += 1
		return tab

	def functions(self):
		tab = []
		regex = re.compile('(function)( )((?:[a-z][a-z0-9_]*))',re.IGNORECASE|re.DOTALL)
		m = regex.findall(self._content_file)
		for n in m:
			tab.append(n[2])
		return tab

	def params_functions(self, function):
		tab = {}
		tab["function"] = function
		start_function = self._content_file.find("function " + function, 0)+10+len(function)
		stop_function = self._content_file.find(")", start_function)
		params = self._content_file[start_function:stop_function]
		params = params.split(",")
		i = 1
		for param in params:
			if param != '':
				tab["param" + str(i)] = ''.join(param.split())
			i += 1
		return tab

	def defines(self):
		tab = {}
		regex = re.compile(r"""\bdefine\(\s*('|")(.*)\1\s*,\s*('|")(.*)\3\)\s*;""",re.IGNORECASE|re.DOTALL)
		m = regex.findall(self._content_file)
		for n in m:
			tab[n[1]] = n[3]
		return tab

	def variables(self):
		tab = {}
		regex = re.compile(r'\$(?P<variable>\w+)\s*=\s*"?\'?(?P<value>[^"\';]+)"?\'?;',re.IGNORECASE|re.DOTALL)
		m = regex.findall(self._content_file)
		for n in m:
			tab[n[0]] = n[1]
		return tab

	def compile(self):
		get_classes = self.classes()
		tab = {}
		tab2 = {}
		i = 1
		for classe in get_classes:
			construct = self.construct_class(classe)
			tab["class"+str(i)] = {"construct": {}, "name": classe}
			for cle, valeur in construct.items():
				if cle != "class":
					tab["class"+str(i)]["construct"][cle] = valeur
			i += 1
		get_functions = self.functions()
		i = 1
		for function in get_functions:
			tab2["function"+str(i)] = {"name": function}
			params = self.params_functions(function)
			for cle, valeur in params.items():
				if cle != "function":
					tab2["function"+str(i)][cle] = valeur
			i += 1
		tab3 = self.defines()
		tab4 = self.variables()
		return tab, tab2, tab3, tab4