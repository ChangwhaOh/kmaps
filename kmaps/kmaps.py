"""Main module."""

import random
import string
import ipyleaflet


class Map(ipyleaflet.Map):
    """Class 'Map'

    Args:
        ipyleaflet (_type_): _description_
    """
    def __init__(self, center = [37.5, 127], zoom = 8, **kwargs):
        """_summary_

        Args:
            center (list): _description_
            zoom (int): _description_
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
            url (str): _description_
            name (str): _description_
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
            basemap (str): _description_

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
            data (str): _description_
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
            data (str): _description_
            name (str, optional): _description_. Defaults to 'ShapeFile'.
        """        
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_layer(geojson, name = name, **kwargs)



def generate_random_string(length, upper = False, digit = False, punc = False):
    """Generates a random string of a given length.

    Args:
        length (int): _description_
        upper (bool, optional): _description_. Defaults to False.
        digit (bool, optional): _description_. Defaults to False.
        punc (bool, optional): _description_. Defaults to False.

    Returns:
        str: _description_
    """
    chars = string.ascii_lowercase
    if upper:
        chars += string.ascii_uppercase
    if digit:
        chars += string.digits
    if punc:
        chars += string.punctuation
    
    result_str = ''.join(random.choice(chars) for i in range(length))
    return result_str


def generate_lucky_number(length = 1):
    """_summary_

    Args:
        length (int, optional): _description_. Defaults to 1.

    Returns:
        int: _description_
    """    
    result_str = ''.join(random.choice(string.digits) for i in range(length))
    result_str = int(result_str)
    return result_str
