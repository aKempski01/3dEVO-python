import os
import argparse
import time

from MainCotroller import MainCotroller


def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


parser = argparse.ArgumentParser(description = 'Application allowing to solve 2d/3d decision game problems.')
parser.add_argument('--yaml-path', type=file_path, help='path to the YAML configuration file. If left empty the default configuration will be used.')

args = parser.parse_args()


def main():
    if args.yaml_path is not None:
        yaml_path = args.yaml_path
    else:
        yaml_path = "data.yml"

    mc = MainCotroller(yaml_path)
    t = time.time()
    mc.run()
    print("The full evolution process took {} seconds".format(time.time() - t))



if __name__ == "__main__":
    main()

