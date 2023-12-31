import numpy as np
from panda3d.core import Vec3

from metadrive.utils.math_utils import Vector
from metadrive.utils.math_utils import wrap_to_pi

# In MetaDrive, the direction of y axis is adverse to Panda3d. It is required to use these function to transform when sync
# the two coordinates.
# MetaDrive (left handed):
#                     ^ x
#                     |
#                     |
#                     |----------> y
#                    Ego
#
# Panda3d (right handed):
#                     ^ x
#                     |
#                     |
#         y <---------|
#                    Ego
# Note: the models loaded in Panda3d are facing to y axis, and thus -90' is required to make it face to x axis


def right_hand_to_left_vector(vector):
    """
    MetaDrive is in left-handed coordinate, while Panda3D and some dataset like Waymo is right-handed coordinate
    """
    vector = np.array(vector, copy=True)
    if vector.ndim == 1:
        vector[1] *= -1
    elif vector.ndim == 2:
        vector[:, 1] *= -1
    else:
        raise ValueError()
    return vector


def left_hand_to_right_hand_vector(vector):
    return right_hand_to_left_vector(vector)


def right_hand_to_left_hand_heading(heading):
    return -heading


def left_hand_to_right_hand_heading(heading):
    return -heading


def panda_vector(position, z=0.0) -> Vec3:
    """
    Give a 2d or 3d position in MetaDrive, transform it to Panda3d world.
    If the position is a 2d array, height will be determined by the value of z.
    if the position is a 3d array, the value of z will be invalid.
    :param position: 2d or 3d position
    :param z: the height of the position, when position is a 2d array
    :return: position represented in Vec3
    """
    if len(position) == 3:
        z = position[2]
    return Vec3(position[0], -position[1], z)


def metadrive_vector(position: Vec3) -> "Vector":
    """
    Transform the position in Panda3d to MetaDrive world
    :param position: Vec3, position in Panda3d
    :return: 2d position
    """
    # return np.array([position[0], -position[1]])
    # return position[0], -position[1]
    return Vector((position[0], -position[1]))


def panda_heading(heading: float) -> float:
    """
    Transform the heading in MetaDrive to Panda3d
    :param heading: float, heading in MetaDrive (degree)
    :return: heading (degree)
    """
    return -heading


def metadrive_heading(heading: float) -> float:
    """
    Transform the heading in Panda3d to MetaDrive
    :param heading: float, heading in panda3d (degree)
    :return: heading (degree)
    """
    return -heading


def waymo_to_metadrive_vector(vector):
    return right_hand_to_left_vector(vector)


# Compatibility
waymo_2_metadrive_position = waymo_to_metadrive_vector


def waymo_to_metadrive_heading(heading, coordinate_transform=True):
    heading = wrap_to_pi(heading)
    if coordinate_transform:
        return -heading
    else:
        return heading


# Compatibility
waymo_2_metadrive_heading = waymo_to_metadrive_heading


def nuplan_to_metadrive_vector(vector, nuplan_center=(0, 0)):
    "All vec in nuplan should be centered in (0,0) to avoid numerical explosion"
    vector = np.array(vector)
    if len(vector.shape) == 1:
        vector[1] *= -1
    else:
        vector[:, 1] *= -1
    vector -= nuplan_center
    return vector


def metadrive_to_nuplan_vector(vector, nuplan_center=(0, 0)):
    "All vec in nuplan should be centered in (0,0) to avoid numerical explosion"
    vector = np.array(vector)
    vector += nuplan_center
    if len(vector.shape) == 1:
        vector[1] *= -1
    else:
        vector[:, 1] *= -1
    return vector


def nuplan_to_metadrive_heading(heading):
    return -wrap_to_pi(heading)


def metadrive_to_nuplan_heading(heading):
    return -wrap_to_pi(heading)
