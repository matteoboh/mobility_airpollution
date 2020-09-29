import numpy as np
import osmnx as ox

###########################################################################################################
############################################# UTILS #######################################################
###########################################################################################################

def map_road_to_attribute(list_roads, road_network, attribute_name, default_value):
	"""Maps each road of a list to the given attribute.

		Parameters
		----------
		list_roads : list
			a list of lists of nodes IDs.

		road_network : networkx MultiDiGraph
			the road network from which to extract the road attributes.

		attribute_name : str
			the name of the attribute.

		default_value : string or int
			the value to return if the attribute is not found.

		Returns
		-------
		Dictionary
			dictionary that maps each road (u,v) to its value of the attribute.
		"""

	''' -- too slow --
	dict_road_to_attribute = {(u,v): data.get(attribute_name, default_value) for u, v, k, data in
									ox.get_undirected(road_network).edges(keys=True, data=True) if
									[u, v] in list_roads}
	'''

	road_network_undirected = ox.get_undirected(road_network)
	dict_road_to_attribute = {}
	for c_road in list_roads:
		c_road_ = (c_road[0], c_road[1])
		c_dict_attributes = road_network_undirected.get_edge_data(c_road[0], c_road[1], key=0, default=default_value)
		if type(c_dict_attributes) == dict:
			c_attribute = c_dict_attributes.get(attribute_name, default_value)
		else:
			c_attribute = default_value
		dict_road_to_attribute[c_road_] = c_attribute

	return dict_road_to_attribute


def normalize_emissions(tdf_with_emissions, percentage=True, list_of_pollutants=['CO_2', 'NO_x', 'PM', 'VOC']):
	"""Normalize values of emissions of the pollutants.

	Parameters
	----------
	tdf_with_emissions : TrajDataFrame
		TrajDataFrame with 4 columns ['CO_2', 'NO_x', 'PM', 'VOC'] collecting the instantaneous emissions for each point.

	percentage : bool
		whether one wants the result as a percentage or not.

	list_of_pollutants : list
		the list of pollutants for which one wants to normalize.

	Returns
	-------
	DataFrame
		a DataFrame containing the normalized values of emissions for each of the pollutants.
	"""

	tdf_with_normalized_emissions = tdf_with_emissions.copy()
	for c_pollutant in list_of_pollutants:
		tot_emissions = float(np.sum(tdf_with_emissions[c_pollutant]))
		if percentage:
			tdf_with_normalized_emissions[c_pollutant] = tdf_with_emissions[c_pollutant] / tot_emissions * 100
		else:
			tdf_with_normalized_emissions[c_pollutant] = tdf_with_emissions[c_pollutant] / tot_emissions
	return tdf_with_normalized_emissions