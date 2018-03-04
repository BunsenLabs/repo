from apt.sourcemgr import EXIT_SUCCESS, EXIT_FAILURE, TEMPLATE_DIR
from jinja2 import FileSystemLoader, Environment
import shlex
import sys
import yaml

def main() -> int:
    try:
        with open(OPTION_SPECPATH, "r") as FILE:
            spec = yaml.load(FILE)
        env = Environment(loader=FileSystemLoader(TEMPLATE_DIR),
                trim_blocks=True)

        dashed_options = [ shlex.quote(" ".join(opt['names']))
                for opt in spec['options'] if len(opt['names']) > 1 ]
        dashed_options = " ".join(dashed_options)

        verb_options = [ shlex.quote(opt['names'][0])
                for opt in spec['options'] if len(opt['names']) == 1 ]
        verb_options = " ".join(verb_options)

        template = env.get_template("bash_completion.jinja")
        print(template.render(dashed_options=dashed_options,
            verb_options=verb_options))
    except Exception as err:
        print(err, file=sys.stderr)
        return EXIT_FAILURE
    return EXIT_SUCCESS
