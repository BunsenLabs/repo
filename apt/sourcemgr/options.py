from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Namespace
import os
import yaml

def get() -> Namespace:
        specpath = os.path.dirname(os.path.abspath(__file__)) + "/options.yml"
        with open(specpath, "r") as FILE:
                spec = yaml.load(FILE)
        p = ArgumentParser(description = spec['program_description'],
                        formatter_class = ArgumentDefaultsHelpFormatter)
        for opt in spec['options']:
                args = opt['names']
                p.add_argument(*opt['names'],
                                **{k:v for k,v in opt.items() if k != 'names'})
        return p.parse_args()
