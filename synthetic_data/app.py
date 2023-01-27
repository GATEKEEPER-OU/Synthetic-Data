import uuid
from argparse import ArgumentParser, Namespace

from synthetic_data.generator.generator import SyntheticDataGenerator


def setup_argparser():
  arg_parser = ArgumentParser(
    # TODO
    # description = '',
    # epilog = ''
  )
  #
  arg_parser.add_argument('-p', '--n-patients',
    type=int, default=1,
    help="Number of patients to generate")
  #
  arg_parser.add_argument('-d', '--n-days',
    type=int, default=1,
    help="Number of days to generate")
  #
  return arg_parser

def main():
  arg_parser = setup_argparser()
  args = arg_parser.parse_args()
  print("aaaaaaaa")
  print(args)

  bundle_path = ''
  sdg = SyntheticDataGenerator(bundle_path)
  sdg.generate()

if __name__=="__main__":
  main()
