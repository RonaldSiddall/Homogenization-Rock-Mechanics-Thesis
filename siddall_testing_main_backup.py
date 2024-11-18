import Generator_DFN_2D_backup
import Testovani_backup
from bgem.stochastic.fr_set import FractureSet

def main_testing_siddall():
    geometry_dict = {
        'box_dimensions': [1, 1, 1],
        'center_depth': 5000,
        'fracture_mesh_step': 1,
        'n_frac_limit': 1200}

    fracture_stats = dict(
        NS={'concentration': 17.8,
            'p_32': 0.094,
            'plunge': 1,
            'power': 2.5,
            'r_max': 564,
            'r_min': 0.038,
            'trend': 292},
        NE={'concentration': 14.3,
            'p_32': 0.163,
            'plunge': 2,
            'power': 2.7,
            'r_max': 564,
            'r_min': 0.038,
            'trend': 326},
        NW={'concentration': 12.9,
            'p_32': 0.098,
            'plunge': 6,
            'power': 3.1,
            'r_max': 564,
            'r_min': 0.038,
            'trend': 60},
        EW={'concentration': 14.0,
            'p_32': 0.039,
            'plunge': 2,
            'power': 3.1,
            'r_max': 564,
            'r_min': 0.038,
            'trend': 15},
        HZ={'concentration': 15.2,
            'p_32': 0.141,
            'power': 2.38,
            'r_max': 564,
            'r_min': 0.038,
            # 'trend': 5
            # 'plunge': 86,
            'strike': 95,
            'dip': 4
            })
    fractures_list = Generator_DFN_2D.plot_dfn(3)
    fractures = FractureSet.from_list(fractures_list)
    Testovani.make_mesh(geometry_dict, fractures, "mine_mesh")
    # n_frac_limit = geometry_dict["n_frac_limit"]
    # statistics = fracture_stats["NS"]
    #fractures = Testovani.generate_uniform(statistics,n_frac_limit)
    #Testovani.plot_fr_orientation(fractures)
    #Testovani.create_fractures_rectangles()
if __name__ == "__main__":
    main_testing_siddall()
