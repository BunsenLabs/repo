from apt.sourcemgr import EXIT_SUCCESS, EXIT_FAILURE, OPTION_SPECPATH
from jinja2 import PackageLoader, Environment
import shlex
import sys
import yaml

def main() -> int:
    try:
        with open(OPTION_SPECPATH, "r") as FILE:
            spec = yaml.load(FILE)
        env = Environment(loader=PackageLoader("apt.sourcemgr"))

        dashed_options = [ shlex.quote(" ".join(opt['names']))
                for opt in spec['options'] if len(opt['names']) > 1 ]
        dashed_options = " ".join(dashed_options)

        verb_options = [ shlex.quote(" ".join(opt['choices']))
                for opt in spec['options'] if "verb" in opt['names'] ]
        verb_options = " ".join(verb_options)

        template = env.get_template("bash_completion.jinja")
        print(template.render(dashed_options=dashed_options,
            verb_options=verb_options))
    except Exception as err:
        print(err, file=sys.stderr)
        return EXIT_FAILURE
    return EXIT_SUCCESS
