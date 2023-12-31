from typing import Sequence, Tuple
from panda3d.core import NodePath
from metadrive.base_class.base_object import BaseObject

LaneIndex = Tuple[str, str, int]


class BaseStaticObject(BaseObject):
    MASS = 1
    HEIGHT = None

    def __init__(self, lane, position: Sequence[float], heading_theta: float = 0., random_seed=None):
        """
        :param lane: the lane to spawn object
        :param position: cartesian position of object in the surface
        :param heading_theta: the angle from positive direction of horizontal axis
        """
        super(BaseStaticObject, self).__init__(random_seed=random_seed)
        self.set_position(position, self.HEIGHT / 2 if hasattr(self, "HEIGHT") else 0)
        self.set_heading_theta(heading_theta)
        self.lane_index = lane.index
        self.lane = lane

    def show_coordinates(self):
        if self.coordinates_debug_np is not None:
            return
        height = self.HEIGHT
        self.coordinates_debug_np = NodePath("debug coordinate")
        x = self.engine.add_line([0, 0, height], [2, 0, height], [1, 0, 0, 1], 1)
        y = self.engine.add_line([0, 0, height], [0, 1, height], [1, 0, 0, 1], 1)
        z = self.engine.add_line([0, 0, height], [0, 0, height + 0.5], [0, 0, 1, 1], 2)
        x.reparentTo(self.coordinates_debug_np)
        y.reparentTo(self.coordinates_debug_np)
        z.reparentTo(self.coordinates_debug_np)
        self.coordinates_debug_np.reparentTo(self.origin)
