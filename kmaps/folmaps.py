"""Folium module."""

import random
import string
import folium


class Map(folium.Map):
    """Class 'Map'.

    Args:
        folium (_type_): Map object from folium.
    """
    def __init__(self, location = [37.5, 127], zoom_start = 8, **kwargs): 
        """Create a Map.

        Args:
            location (list, optional): A coordinate representing the center of the map. Defaults to `[37.5, 127]`
            zoom_start (int, optional): Zoom level. Defaults to 8
        """            
        if 'scroll_wheel_zoom' not in kwargs:
            kwargs['scroll_wheel_zoom'] = True
        super().__init__(location = location, zoom_start = zoom_start, **kwargs) # inherited from the parent, in this case, ipyleaflet


    def add_layers_control(self, **kwargs):
        """Add a layers control panel to the map.
        """        
        folium.LayerControl(**kwargs).add_to(self)


    def add_geojson(self, data, name = 'GeoJSON', **kwargs):
        """Add a geojson file to the map (folium version).

        Args:
            data (str): A name of the geojson file.
            name (str, optional): A layer name of the geojson file to be displayed on the map. Defaults to 'GeoJSON'.
        """     
        folium.GeoJson(data, name = name).add_to(self)
    
    def add_shp(self, data, name = 'Shapefile', **kwargs):
        """Add a ESRI shape file to the map (folium version).

        Args:
            data (str): A name of the shape file.
            name (str, optional): A layer name of the shape file to be displayed on the map. Defaults to 'Shapefile'.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name = name, **kwargs)
    

    def add_tile_layer(self, url, name, attr = 'Tile', **kwargs):
        """Add a tile layer to the map.

        Args:
            url (str): xyz url of the tile layer.
            name (str): A name of the layer that would be displayed on the map.
            attr (str, optional): A name of the attribution. Defaults to 'Tile'.
        """        
        tile_layer = folium.TileLayer(
            tiles = url,
            name = name,
            attr = attr,
            **kwargs
        )

        self.add_child(tile_layer)


    def add_basemap(self, basemap, **kwargs):
        """Add a base map to the map.

        Args:
            basemap (str): xyz url of the base map.

        Raises:
            ValueError: Error message will be raised if the url is not available.
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
                self.add_tile_layer(url, name = basemap, attr = attribution, **kwargs)
            except:
                raise ValueError(f'{basemap} is not found')