from PIL import Image
from PIL import ImageDraw
import numpy as np
from bgem.stochastic import dfn


# I have no idea how or why this works or what it´s used for, but it seems to change the scale somehow?
def scale_cut(x, s):
    return tuple([max(0, min(sv, int(sv * xv))) for xv, sv in zip(x[:2], s)])


def plot_dfn(power):
    s = (1000, 1000)

    im = Image.new('RGBA', s, (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    fracture_box = [1, 1, 1]
    sample_range = (0.001, 1)
    power = 2.1
    conf_range = [0.001, 1]
    p_32 = 3.1
    # p_32 = 0.094
    size = dfn.PowerLawSize.from_mean_area(power - 1, conf_range, p_32, power)
    family = dfn.FrFamily(
        orientation=dfn.FisherOrientation(0, 90, 0),
        size=size,
        shape_angle=dfn.VonMisesOrientation(0, 0)
    )
    pop = dfn.Population(
        domain=(fracture_box[0], fracture_box[1], 0),
        families=[family]
    )
    pop.set_sample_range(sample_range)
    pos_gen = dfn.UniformBoxPosition(fracture_box)
    print("total mean size: ", pop.mean_size())

    fractures = pop.sample(pos_distr=pos_gen, keep_nonempty=True)
    print("N frac:", len(fractures))
    sizes = []
    for fr in fractures:
        t = 0.5 * fr.r * np.array([-fr.normal[2], fr.normal[1], 0])
        a = scale_cut(0.5 + fr.center - t, s)
        b = scale_cut(0.5 + fr.center + t, s)
        draw.line((a, b), fill=(0, 0, 0), width=1)
        sizes.append(fr.r)

    # plot_sizes(sizes, sample_range, pop.families[0].size)

    # ax.imshow(np.asarray(im),  origin='lower')
    im.show()
    return fractures


if __name__ == "__main__":
    plot_dfn(2.5)
