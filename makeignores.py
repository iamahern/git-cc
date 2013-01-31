
#
# CuramDev specific
#
from common import *
from clearcase import cc
import os

GIT_PRIVATE = frozenset(['.git', '.gitignore'])

ARGS = {
	'checkfrom' : 'Directory to scan for ignores from. If not specified, this will scan from the current directory'
}

def main(checkfrom='.'):
	tdirs = 0;
	# Clear Case dir is => CC_DIR
	for root, dirs, files in os.walk(os.path.abspath(checkfrom)):
		# view_only files
		pfilesdirs = get_view_private(root)
		# list to print to .gitignore
		ignores = []
		
		# process files
		for f in files[:]:
			if f in pfilesdirs and f not in GIT_PRIVATE:
				ignores.append("/" + f)
		
		# process dirs
		dirs2skip = []
		for d in dirs[:]:
			if d in GIT_PRIVATE:
				dirs2skip.append(d)
			elif d in pfilesdirs:
				ignores.append("/" + d + "/")
				dirs2skip.append(d)
		for toskip in dirs2skip[:]:
			dirs.remove(toskip)
		
		# ensure stable
		ignores = sorted(ignores, key=str.lower)
		gitignoresFileName = root + os.sep + '.gitignore'
		
		if len(ignores) > 0:
			# Write ignorefile
			gitignoresFile = open(gitignoresFileName, 'w')
			gitignoresFile.write("\n".join(ignores))
		elif os.path.isfile(gitignoresFileName):
			os.remove(gitignoresFileName)
			
#
# Find the view_only files and normalize the file names
#
def get_view_private(root):
	res = cc_exec(['ls', '-view_only', root]).decode("utf-8").splitlines()

	for i, item in enumerate(res):
		res[i] = item.rpartition(os.sep)[2]

	return set(res)

