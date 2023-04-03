"""Main module."""

import random
import string
import numpy as np
import ipyleaflet


class Map(ipyleaflet.Map):
    """Class 'Map'

    Args:
        ipyleaflet (_type_): _description_
    """
    def __init__(self, center, zoom, **kwargs):
        """_summary_

        Args:
            center (_type_): _description_
            zoom (_type_): _description_
        """        
        if 'scroll_wheel_zoom' not in kwargs:
            kwargs['scroll_wheel_zoom'] = True
        super().__init__(center = center, zoom = zoom, **kwargs) # inherited from the parent, in this case, ipyleaflet
    
    def add_search_control(self, position = 'topleft', **kwargs):
        """_summary_

        Args:
            position (str, optional): _description_. Defaults to 'topleft'.
        """        
        if 'url' not in kwargs:
            kwargs['url'] = 'https://nominatim.openstreetmap.org/search?format=json&q={s}'
        
        search_control = ipyleaflet.SearchControl(position = position, **kwargs)
        self.add_control(search_control)

    def add_draw_control(self, **kwargs):
        draw_control = ipyleaflet.DrawControl(**kwargs)
        self.add_control(draw_control)



def euclidean_dist(first_coord, second_coord):
    """_summary_

    Args:
        first_coord (list): _description_
        second_coord (list): _description_

    Returns:
        _type_: _description_
    """
    if len(first_coord) != 2:
        print('1')
        break
    if len(second_coord) != 2:
        print('2')
        break
    x_diff = first_coord[0] - second_coord[0]
    y_diff = first_coord[1] - second_coord[1]
    dist = np.sqrt((x_diff) ** 2 + (y_diff) ** 2)
    return dist