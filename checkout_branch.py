import sys
import os
import time

class GitCheckoutTools(object):
	def __init__(self):
		self.init_git_dirs()

	def init_git_dirs(self):
		self.git_dirs = []
		cwd = os.getcwd()

		self.git_dirs.append(cwd+"/assets/app_identify")
		self.git_dirs.append(cwd+"/assets/asset_main")
		self.git_dirs.append(cwd+"/assets/identify_plugin")
		self.git_dirs.append(cwd+"/assets/include")
		self.git_dirs.append(cwd+"/assets/local_cache")
		self.git_dirs.append(cwd+"/assets/utility")
		#self.git_dirs.append(cwd+"/assets/web_frameworks")

		self.git_dirs.append(cwd+"/bin")
		self.git_dirs.append(cwd+"/build")
		self.git_dirs.append(cwd+"/compile")
		self.git_dirs.append(cwd+"/config")
		self.git_dirs.append(cwd+"/include")
		self.git_dirs.append(cwd+"/src_public")


	def git_checkout(self, branch):
		for git_dir in self.git_dirs:
			os.chdir(git_dir)
			#os.system("git pull") 
			if(0 == os.system("git checkout " + branch)):
				print("checkout " + git_dir + " directory " + branch + " success")
				os.system("git pull")
				return True
			else:
				print("checkout " + git_dir + " directory" + branch + " failed")
				return False
def main(argc, argv):
	if argc < 3:
		return False
	else:
		print("dir: " + argv[1] + " branch: " + argv[2])
		os.chdir(argv[1]);
		git = GitCheckoutTools()
		git.git_checkout(argv[2])
		return True
if __name__ == '__main__':
	if(False == main(len(sys.argv), sys.argv)):
		os.chdir(os.path.dirname(__file__))
		branch = str(os.path.splitext(os.path.basename(__file__))[0])
		print("checkout " + branch + " branch")
		git = GitCheckoutTools()
		git.git_checkout(branch)
		time.sleep(10)		