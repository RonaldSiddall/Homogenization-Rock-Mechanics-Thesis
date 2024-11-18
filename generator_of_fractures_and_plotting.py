from PIL import Image, ImageDraw
import numpy as np
from bgem.stochastic import dfn


def scale_cut(x, s):
    """Scales and cuts the coordinates based on the defined width and height."""
    return tuple([max(0, min(sv, int(sv * xv))) for xv, sv in zip(x[:2], s)])


def plotting_of_dfn(parameters, fractures):
    amount_of_pixels = parameters["image_parameters"]["amount_of_pixels"]
    image_background_colour = parameters["image_parameters"]["image_background_colour"]
    colour_of_fractures = parameters["image_parameters"]["colour_of_fractures"]
    width_of_fractures = parameters["image_parameters"]["width_of_fractures"]

    image = Image.new('RGBA', amount_of_pixels, image_background_colour)
    draw = ImageDraw.Draw(image)
    for fr in fractures:
        # it used to be t = 0.5 * fr.r * np.array([-fr.normal[2], fr.normal[1], 0]),
        # but I would get vertical lines only, I guess because of the z component being zero
        t = 0.5 * fr.r * np.array([-fr.normal[1], fr.normal[0], 0])
        a = scale_cut(0.5 + fr.center - t, amount_of_pixels)
        b = scale_cut(0.5 + fr.center + t, amount_of_pixels)
        draw.line((a, b), fill=colour_of_fractures, width=width_of_fractures)
    image.show()


def fractures_generation(parameters):
    fracture_box = parameters["fracture_parameters"]["fracture_box"]
    sample_range = parameters["fracture_parameters"]["sample_range"]
    power = parameters["fracture_parameters"]["power"]
    conf_range = parameters["fracture_parameters"]["conf_range"]
    p_32 = parameters["fracture_parameters"]["p_32"]
    fisher_trend = parameters["statistics_parameters"]["fisher_orientation_parameters"]["fisher_trend"]
    fisher_plunge = parameters["statistics_parameters"]["fisher_orientation_parameters"]["fisher_plunge"]
    fisher_concentration = parameters["statistics_parameters"]["fisher_orientation_parameters"]["fisher_concentration"]
    von_mises_trend = parameters["statistics_parameters"]["von_mises_parameters"]["von_mises_trend"]
    von_mises_concentration = parameters["statistics_parameters"]["von_mises_parameters"]["von_mises_concentration"]

    size = dfn.PowerLawSize.from_mean_area(power - 1, conf_range, p_32, power)

    family_of_fractures = dfn.FrFamily(
        orientation=dfn.FisherOrientation(fisher_trend, fisher_plunge, fisher_concentration),
        size=size,
        shape_angle=dfn.VonMisesOrientation(von_mises_trend, von_mises_concentration)
    )

    population_of_fractures = dfn.Population(domain=(fracture_box[0], fracture_box[1], 0),
                                             families=[family_of_fractures])
    population_of_fractures.set_sample_range(sample_range)
    position_generator = dfn.UniformBoxPosition(fracture_box)

    fractures = population_of_fractures.sample(pos_distr=position_generator, keep_nonempty=True)

    # GOAL: set normal z component to zero for each fracture
    updated_fractures = []
    for fr in fractures:
        fr.normal = np.array([fr.normal[0], fr.normal[1], 0])
        updated_fractures.append(fr)
    print(f"Information about the first fracture for reference:{updated_fractures[0]}")
    print(f"First fracture shape_angle value:{updated_fractures[0].shape_angle}")
    plotting_of_dfn(parameters, updated_fractures)
    return updated_fractures
