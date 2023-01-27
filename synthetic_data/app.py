import logging
import os
from argparse import ArgumentParser, Namespace

from synthetic_data.generator.generator import SyntheticDataGenerator
from synthetic_data.globals import (BUNDLE_PATH_DEFAULT, NUM_DAYS_MAX,
                                    NUM_DAYS_MIN, NUM_PATIENTS_MAX,
                                    NUM_PATIENTS_MIN)


def setup_argparser():
  arg_parser = ArgumentParser(
    # TODO
    # description = '',
    # epilog = ''
  )
  #
  arg_parser.add_argument('-b', '--bundle-dir',
    type=str, default=BUNDLE_PATH_DEFAULT,
    help="Path of the bundle directory")
  #
  arg_parser.add_argument('-o', '--output-dir',
    type=str, default=BUNDLE_PATH_DEFAULT,
    help="Path of the output directory")
  #
  arg_parser.add_argument('-p', '--n-patients',
    type=int, default=NUM_PATIENTS_MIN,
    help="Number of patients to generate")
  #
  arg_parser.add_argument('-d', '--n-days',
    type=int, default=NUM_DAYS_MIN,
    help="Number of days to generate")
  #
  return arg_parser

def check_args(args: Namespace):
  #
  bundle_dir = str(args.bundle_dir)
  if not os.path.exists(bundle_dir):
    # raise ValueError("'%s' not exists" % bundle_dir) // TODO enable this
    pass
  #
  output_dir = str(args.output_dir)
  if not os.path.exists(output_dir):
    # raise ValueError("'%s' not exists" % output_dir)
    os.makedirs(output_dir)
  #
  n_patients = int(args.n_patients)
  if not NUM_PATIENTS_MIN <= n_patients <= NUM_PATIENTS_MAX:
    raise ValueError("The number of patients must be included in %d and %d. '%d' given."
      % (NUM_PATIENTS_MIN, NUM_PATIENTS_MAX, n_patients))
  #
  n_days = int(args.n_days)
  if not NUM_DAYS_MIN <= n_days <= NUM_DAYS_MAX:
    raise ValueError("The number of patients must be included in %d and %d. '%d' given."
      % (NUM_DAYS_MIN, NUM_DAYS_MAX, n_days))

def main():
  logger = logging.getLogger()
  #
  try:
    arg_parser = setup_argparser()
    args = arg_parser.parse_args()
    # print(args) # DEBUG
    check_args(args)

    sdg = SyntheticDataGenerator(args.bundle_dir)
    sdg.generate(args.output_dir, args.n_patients, args.n_patients)
  #
  except ValueError as e:
    logger.error("%s" % e)
  except Exception:
    logger.error("Interrupted:", exc_info=True)


if __name__=="__main__":
  main()
