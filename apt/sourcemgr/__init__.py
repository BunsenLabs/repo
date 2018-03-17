import apt_pkg
import os

APT_SOURCE_PARTSDIR = apt_pkg.config.find_dir("Dir::Etc::sourceparts")
EXIT_FAILURE        = 1
EXIT_NOMATCH        = 2
EXIT_SUCCESS        = 0
OPTION_SPECPATH     = os.path.dirname(os.path.abspath(__file__)) + "/options.yml"
