import numpy as np
from bgem.stochastic import dfn, fr_set
from bgem.stochastic.fr_set import FractureSet


def generator_of_fracture_set(parameters):
    rectangle_dimensions = parameters["geometry_parameters"]["rectangle_dimensions"]
    sample_range = parameters["fracture_parameters"]["sample_range"]
    k_r = parameters["fracture_parameters"]["k_r"]
    diam_range = parameters["fracture_parameters"]["diam_range"]
    p32_r_0_to_infty = parameters["fracture_parameters"]["p32_r_0_to_infty"]
    fisher_trend = parameters["statistics_parameters"]["fisher_orientation_parameters"]["fisher_trend"]
    fisher_plunge = parameters["statistics_parameters"]["fisher_orientation_parameters"]["fisher_plunge"]
    fisher_concentration = parameters["statistics_parameters"]["fisher_orientation_parameters"]["fisher_concentration"]
    von_mises_trend = parameters["statistics_parameters"]["von_mises_parameters"]["von_mises_trend"]
    von_mises_concentration = parameters["statistics_parameters"]["von_mises_parameters"]["von_mises_concentration"]

    power = k_r - 3
    size = dfn.PowerLawSize.from_mean_area(power, diam_range, p32_r_0_to_infty)
    family_of_fractures = dfn.FrFamily(
        orientation=dfn.FisherOrientation(fisher_trend, fisher_plunge, fisher_concentration),
        size=size,
        shape_angle=dfn.VonMisesOrientation(von_mises_trend, von_mises_concentration)
    )
    size.set_sample_range(sample_range)
    domain = (rectangle_dimensions[0], rectangle_dimensions[1], 0)
    population_of_fractures = dfn.Population(domain= domain,
                                             families=[family_of_fractures], shape=fr_set.LineShape())
    population_of_fractures.set_sample_range(sample_range)
    dimensions_volume = [rectangle_dimensions[0], rectangle_dimensions[1], 1]
    position_generator = dfn.UniformBoxPosition(dimensions_volume)

    fractures = population_of_fractures.sample(pos_distr=position_generator, keep_nonempty=True)
    # GOAL: set normal z component to zero for each fracture
    updated_fractures = []
    for fr in fractures:
        fr.normal = np.array([fr.normal[0], fr.normal[1], 0])
        updated_fractures.append(fr)
    # print(f"Information about the first fracture for reference:\n{updated_fractures[0]}")
    # print(f"First fracture shape_angle value:{updated_fractures[0].shape_angle}")
    # print(f"First fracture rotation_angle value:{updated_fractures[0].rotation_angle}")
    # print(f"First fracture rotation_axis value:{updated_fractures[0].rotation_axis}")
    # plotting_of_dfn(parameters, updated_fractures)
    fractures_set = FractureSet.from_list(updated_fractures)
    return fractures_set

