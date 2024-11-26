import sys
from GenerateFractures import GenerateFractures
from GenerateMesh import GenerateMesh


def main(config_file):
    fracture_set = GenerateFractures(config_file).generator_of_fracture_set()
    GenerateMesh(config_file, fracture_set).make_mesh()


if __name__ == "__main__":
    config_file = sys.argv[1]
    main(config_file)