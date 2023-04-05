"""Main module."""

import random
import string
import ipyleaflet

import numpy as np
import pandas as pd
import geopandas as gpd

from shapely.geometry import Polygon


class Map(ipyleaflet.Map): # inherited from ipyleaflet.Map
    """Class 'Map'

    Args:
        ipyleaflet (_type_): _description_
    """
    def __init__(self, center = [37.5, 127], zoom = 8, **kwargs):
        """_summary_

        Args:
            center (_type_): _description_
            zoom (_type_): _description_
        """        
        if 'scroll_wheel_zoom' not in kwargs:
            kwargs['scroll_wheel_zoom'] = True
        super().__init__(center = center, zoom = zoom, **kwargs) # inherited from the parent, in this case, ipyleaflet
        
        if 'layers_control' not in kwargs:
            kwargs['layers_control'] = True
        
        if kwargs['layers_control']:
            self.add_layers_control()

        self.add_search_control()
    


    def add_search_control(self, position = 'topleft', **kwargs):
        """_summary_

        Args:
            position (str, optional): _description_. Defaults to 'topleft'.
        """        
        if 'url' not in kwargs:
            kwargs['url'] = 'https://nominatim.openstreetmap.org/search?format=json&q={s}'
        
        search_control = ipyleaflet.SearchControl(position = position, **kwargs)
        self.add_control(search_control)


    def add_draw_control(self, position = 'topleft', **kwargs):
        """_summary_

        Args:
            position (str, optional): _description_. Defaults to 'topleft'.
        """        
        draw_control = ipyleaflet.DrawControl(position = position, **kwargs)
        self.add_control(draw_control)


    def add_layers_control(self, position = 'topright', **kwargs):
        """_summary_

        Args:
            position (str, optional): _description_. Defaults to 'topright'.
        """        
        layers_control = ipyleaflet.LayersControl(position = position, **kwargs)
        self.add_control(layers_control)


    def add_tile_layer(self, url, name, attribution = '', **kwargs):
        """_summary_

        Args:
            url (_type_): _description_
            name (_type_): _description_
            attribution (str, optional): _description_. Defaults to ''.
        """        
        tile_layer = ipyleaflet.TileLayer(
            url = url,
            name = name,
            attribution = attribution,
            **kwargs
        )
        self.add_layer(tile_layer)
    

    def add_basemap(self, basemap, **kwargs):
        """_summary_

        Args:
            basemap (_type_): _description_

        Raises:
            ValueError: _description_
        """
        import xyzservices.providers as xyz

        if basemap.lower() == 'roadmap':
            url = 'http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name = basemap, **kwargs)
        elif basemap.lower() == 'satellite':
            url = 'http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name = basemap, **kwargs)
        else:
            try:
                basemap = eval(f'xyz.{basemap}')
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url, name = basemap, attribution = attribution, **kwargs)
            except:
                raise ValueError(f'{basemap} is not found')


    def add_geojson(self, data, name = 'GeoJSON', **kwargs):
        """_summary_

        Args:
            data (_type_): _description_
            name (str, optional): _description_. Defaults to 'GeoJSON'.
        """        
        if isinstance(data, str):
            import json
            with open(data, 'r') as f:
                data = json.load(f)

        geojson = ipyleaflet.GeoJSON(data = data, name = name, **kwargs)
        self.add_layer(geojson)


    def add_shp(self, data, name = 'ShapeFile', **kwargs):
        """_summary_

        Args:
            data (_type_): _description_
            name (str, optional): _description_. Defaults to 'ShapeFile'.
        """        
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_layer(geojson, name = name, **kwargs)



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
    elif len(second_coord) != 2:
        print('2')
    else:
        x_diff = first_coord[0] - second_coord[0]
        y_diff = first_coord[1] - second_coord[1]
        dist = np.sqrt((x_diff) ** 2 + (y_diff) ** 2)
        return dist


def random_points_generator(Xls, Yls):
    """_summary_

    Args:
        Xls (list): _description_
        Yls (list): _description_

    Returns:
        _type_: _description_
    """
    XCoord = list(Xls)
    YCoord = list(Yls)

    IDls = []
    for i in range(0, len(Xls)):
        IDls.append(i + 1)

    df_dict = {'ID': IDls, 'XCoord': XCoord, 'YCoord': YCoord}
    df = pd.DataFrame(df_dict)
    df = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(XCoord, YCoord))

    return df