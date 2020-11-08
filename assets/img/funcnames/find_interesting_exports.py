#!/usr/bin/env python
# Script to discover interesting exports in DLLs.
# You can use this script in any way you want.
# http://ashutoshmehra.net/blog/

import os, pefile, re, collections

# Globals
dll_root_dir = 'c:/Windows'
interesting_copyright_re = re.compile('Microsoft')
cpp_fname_re = re.compile('[@_]')
min_interesting_func_len = 40
len_stats = collections.defaultdict(int)
max_func_name_len = 60

# Checks file extension for dll
def is_a_dll(file_name):
	return os.path.splitext(file_name)[-1].lower() == '.dll'

# Returns LegalCopyright property (or the empty string)
def get_copyright(pe_obj):
	copyrights = [t[1] for e in getattr(pe_obj, 'FileInfo', [])
				  for s in getattr(e, 'StringTable', [])
				  for t in s.entries.items() if t[0] == u'LegalCopyright']
	if len(copyrights) == 0:
		return ''
	else:
		return copyrights[0].encode('iso-8859-15', 'replace')

# Checks if this is a "system" DLL (by groking the Copyright string)
def is_interesting_dll(file_name):
	try:
		p = pefile.PE(file_name)
		p.parse_data_directories([pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_RESOURCE']])
		return interesting_copyright_re.search(get_copyright(p)) != None
	except pefile.PEFormatError:
		return False

# Identifies suspected C++ish exports
def is_cpp_kinda_export(func_name):
	return cpp_fname_re.search(func_name) != None

# Checks for exports with long names
def is_interesting_export(func_name):
	return len(func_name) >= min_interesting_func_len
		
def dump_exports(file_name):
	try:
		p = pefile.PE(file_name)
		p.parse_data_directories([pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT']])
		for e in p.DIRECTORY_ENTRY_EXPORT.symbols:
			if e.name != None and not is_cpp_kinda_export(e.name):
				len_stats[len(e.name)] += 1
				if is_interesting_export(e.name):
					print '%d, %s, %s' % (len(e.name), e.name, file_name)
	except (AttributeError, pefile.PEFormatError):
		pass

def walk_dir_for_interesting_function_names(root):
	pefile.fast_load = True
	for (dirpath, dirnames, filenames) in os.walk(root):
		for f in filenames:
			f = os.path.join(dirpath, f)
			if is_a_dll(f) and is_interesting_dll(f):
				dump_exports(f)

# Dump Stats
walk_dir_for_interesting_function_names(dll_root_dir)
file('func_len_stats', 'w').writelines([("%d, %d\n" % (i, len_stats[i])) for i in range(max_func_name_len)])
