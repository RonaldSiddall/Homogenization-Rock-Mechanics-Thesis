import numpy as np
from bgem.stochastic.fr_set import FractureSet
from bgem.stochastic import dfn, fr_set
from Logic_classes.ConfigManager import ConfigManager
from Utility_methods.check_values_in_config_file import check_values_in_config_file_mesh

class GenerateFractures:
    # Initiation of the used parameters from the config.yaml file
    def __init__(self, config_file):
        # This checks the values within the config file before generating the fractures
        # If any parameter is invalid, everything is skipped
        control_variable = check_values_in_config_file_mesh(config_file)
        if control_variable is False:
            return

        # Loading of needed values from the config file
        self.config = ConfigManager(config_file)
        self.rectangle_dimensions = self.config.get_rectangle_dimensions()
        self.sample_range = self.config.get_sample_range()
        self.k_r = self.config.get_k_r()
        self.diam_range = self.config.get_diam_range()
        self.p32_r_0_to_infty = self.config.get_p32_r0_to_r_infty()
        self.fisher_trend = self.config.get_fisher_trend()
        self.fisher_plunge = self.config.get_fisher_plunge()
        self.fisher_kappa = self.config.get_fisher_kappa()
        self.von_mises_trend = self.config.get_von_mises_trend()
        self.von_mises_kappa = self.config.get_von_mises_kappa()

    def generator_of_fracture_set(self):
        """
        Generates a FractureSet object containing the generated fractures (objects of type Fracture),
        based on the configuration parameters
        """

        # Generates size distribution based on power law and diameter range
        size = dfn.PowerLawSize.from_mean_area(self.k_r, self.diam_range, self.p32_r_0_to_infty)

        # Sets sample range for fracture sizes
        size.set_sample_range(self.sample_range)

        # Defines fracture family properties: orientation and size distribution
        family = dfn.FrFamily(
            orientation=dfn.FisherOrientation(self.fisher_trend, self.fisher_plunge, self.fisher_kappa),
            size=size,
            shape_angle=dfn.VonMisesOrientation(self.von_mises_trend, self.von_mises_kappa),
            name='fractures')

        # Defines the domain of the fractures based on the rectangle dimensions
        domain = (self.rectangle_dimensions[0], self.rectangle_dimensions[1], 0)

        # Creates a population of fractures, using LineShape for the shape
        population_of_fractures = dfn.Population(
            domain=domain,
            families=[family],
            shape=fr_set.LineShape())

        # Sets sample range for population of fractures
        population_of_fractures.set_sample_range(self.sample_range)

        # Defines the volume dimensions (increased Z component for 3D), has to be non-zero, otherwise the number
        # of fractures is equal to 1 (number of fractures tied to volume, for V = 0 => 1 fracture)
        dimensions_volume = [self.rectangle_dimensions[0], self.rectangle_dimensions[1], 1]

        # Position generator for fracture placement within the defined volume
        position_generator = dfn.UniformBoxPosition(dimensions_volume)

        # Samples fractures based on the position distribution
        fractures = population_of_fractures.sample(pos_distr=position_generator, keep_nonempty=True)

        # Sets normal z-component to zero for each fracture
        updated_fractures = []
        for fr in fractures:
            fr.normal = np.array([fr.normal[0], fr.normal[1], 0])
            updated_fractures.append(fr)

        # Creates a FractureSet from the updated_fractures and returns it
        fracture_set = FractureSet.from_list(updated_fractures)
        return fracture_set