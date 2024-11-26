from bgem.stochastic import dfn, fr_set
import numpy as np
from Config_manager import ConfigManager
from bgem.stochastic.fr_set import FractureSet


class GenerateFractures:
    # Initiation of the used parameters from the config.yaml file
    def __init__(self, config_file):
        self.config = ConfigManager(config_file)
        self.rectangle_dimensions = self.config.get_rectangle_dimensions()

        self.sample_range = self.config.get_sample_range()
        self.k_r = self.config.get_k_r()
        self.diam_range = self.config.get_diam_range()
        self.p32_r_0_to_infty = self.config.get_p32_r_0_to_infty()

        self.fisher_trend = self.config.get_fisher_trend()
        self.fisher_plunge = self.config.get_fisher_plunge()
        self.fisher_concentration = self.config.get_fisher_concentration()

        self.von_mises_trend = self.config.get_von_mises_trend()
        self.von_mises_concentration = self.config.get_von_mises_concentration()

    def generator_of_fracture_set(self):
        """
        Generates a FractureSet object containing the generated fractures (objects of type Fracture),
        based on the configuration parameters
        """

        # Calculates power from k_r parameter - reason in theory...
        power = self.k_r - 3

        # Generates size distribution based on power law and diameter range
        size = dfn.PowerLawSize.from_mean_area(power, self.diam_range, self.p32_r_0_to_infty)

        # Sets sample range for fracture sizes
        size.set_sample_range(self.sample_range)

        # Defines fracture family properties: orientation and size distribution
        family = dfn.FrFamily(
            orientation=dfn.FisherOrientation(self.fisher_trend, self.fisher_plunge, self.fisher_concentration),
            size=size,
            shape_angle=dfn.VonMisesOrientation(self.von_mises_trend, self.von_mises_concentration)
        )

        # Defines the domain of the fractures based on the rectangle dimensions
        domain = (self.rectangle_dimensions[0], self.rectangle_dimensions[1], 0)

        # Creates a population of fractures, using LineShape for the shape
        population_of_fractures = dfn.Population(
            domain=domain,
            families=[family],
            shape=fr_set.LineShape()
        )

        # Sets sample range for population of fractures
        population_of_fractures.set_sample_range(self.sample_range)

        # Defines the volume dimensions (increased Z component for 3D), has to be non-zero, otherwise the amount
        # of fractures is equal to 1 (amount of fractures tied to volume, for V = 0 => 1 fracture)
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

        # Create a FractureSet from the updated_fractures
        fracture_set = FractureSet.from_list(updated_fractures)

        return fracture_set
