import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Updated dictionary of locations with unique coordinates
LOCATIONS = {
    'F-6 Markaz': (0, 0),
    'F-7 Markaz': (2, 1),
    'G-9 Markaz': (-2, 3.5),
    'I-8 Markaz': (-3, 5),
    'E-11 Markaz': (-3, -2),
    'F-10 Markaz': (1, 3),
    'G-11 Markaz': (-1, 4),
    'F-17': (5, 7),
    'E-11': (-3, -3),
    'G-10': (0, 4),
    'D-12': (-5, -1),
    'F-11': (2, 4),
    'G-6': (-1, 1),
    'IIUI': (-6, 6),
    'Air University': (3, 5),
    'FAST University': (1, 2),
    'COMSATS': (4, 3),
    'NUST': (-2, 6),
    'Faisal Mosque': (0, 6),
    'Shakarparian': (3, -1),
    'Pakistan Monument': (2, -2),
    'Daman-e-Koh': (1, 6),
    'Centaurus Mall': (2, 0),
    'Serena Hotel': (1, 1),
    # Added Hospitals (unique locations)
    'PIMS Hospital': (-1, 2.7),
    'Shifa Hospital': (-3, 6.5),
    'Ali Medical Hospital': (3.5, 2),
    # Added Fire Stations (unique locations)
    'Fire Station F-7': (2.5, 0.5),
    'Fire Station G-9': (-2.5, 2.5),
    'Fire Station I-8': (-4.5, 4.5)
}

# Updated distances with multiple connections for hospitals and fire stations
DISTANCES = {
    ('F-6 Markaz', 'F-7 Markaz'): 3,
    ('F-7 Markaz', 'F-10 Markaz'): 4,
    ('F-10 Markaz', 'F-11'): 2,
    ('G-9 Markaz', 'G-10'): 2,
    ('G-10', 'G-11 Markaz'): 3,
    ('E-11 Markaz', 'E-11'): 1,
    ('I-8 Markaz', 'G-9 Markaz'): 5,
    ('F-7 Markaz', 'FAST University'): 3,
    ('G-11 Markaz', 'NUST'): 4,
    ('F-10 Markaz', 'Air University'): 4,
    ('G-9 Markaz', 'COMSATS'): 6,
    ('E-11', 'IIUI'): 8,
    ('F-7 Markaz', 'Centaurus Mall'): 2,
    ('F-6 Markaz', 'Serena Hotel'): 2,
    ('G-10', 'Faisal Mosque'): 3,
    ('F-11', 'Daman-e-Koh'): 4,
    ('F-7 Markaz', 'Pakistan Monument'): 4,
    ('F-6 Markaz', 'Shakarparian'): 5,
    ('G-6', 'F-6 Markaz'): 2,
    ('G-6', 'G-9 Markaz'): 4,
    ('F-10 Markaz', 'G-10'): 2,
    ('F-11', 'E-11'): 5,
    ('D-12', 'E-11'): 3,
    ('F-17', 'Air University'): 4,
    # Connections for hospitals
    ('PIMS Hospital', 'G-9 Markaz'): 2,
    ('PIMS Hospital', 'G-10'): 2,
    ('PIMS Hospital', 'Faisal Mosque'): 3,
    ('Shifa Hospital', 'NUST'): 3,
    ('Shifa Hospital', 'G-11 Markaz'): 2,
    ('Shifa Hospital', 'I-8 Markaz'): 6,
    ('Ali Medical Hospital', 'FAST University'): 2,
    ('Ali Medical Hospital', 'Air University'): 2,
    ('Ali Medical Hospital', 'COMSATS'): 3,
    # Connections for fire stations
    ('Fire Station F-7', 'F-7 Markaz'): 1,
    ('Fire Station F-7', 'Centaurus Mall'): 2,
    ('Fire Station F-7', 'Pakistan Monument'): 3,
    ('Fire Station G-9', 'G-9 Markaz'): 1,
    ('Fire Station G-9', 'G-10'): 2,
    ('Fire Station G-9', 'G-6'): 2,
    ('Fire Station I-8', 'I-8 Markaz'): 1,
    ('Fire Station I-8', 'Shifa Hospital'): 2,
    ('Fire Station I-8', 'G-9 Markaz'): 5
}



# Then modify the visualize_map function in map_visualization.py

import plotly.graph_objects as go



def visualize_map(self, highlight_path=None, distance=None, price=None):
    """
    Visualize the map with locations, distances, and optionally highlight a path.
    """
    plt.figure(figsize=(12, 12))

    for loc, (x, y) in LOCATIONS.items():
        # Differentiate types of locations
        if 'Hospital' in loc:
            plt.scatter(x, y, color='red', label='Hospital' if 'Hospital' not in plt.gca().get_legend_handles_labels()[1] else "", s=200, alpha=0.7)
        elif 'Fire Station' in loc:
            plt.scatter(x, y, color='orange', label='Fire Station' if 'Fire Station' not in plt.gca().get_legend_handles_labels()[1] else "", s=200, alpha=0.7)
        else:
            plt.scatter(x, y, color='blue', label='Location' if 'Location' not in plt.gca().get_legend_handles_labels()[1] else "", s=200, alpha=0.5)
        plt.text(x + 0.3, y + 0.3, loc, fontsize=8)

    for (loc1, loc2), dist in DISTANCES.items():
        x1, y1 = LOCATIONS[loc1]
        x2, y2 = LOCATIONS[loc2]
        plt.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5)
        plt.text((x1 + x2) / 2, (y1 + y2) / 2, f'{dist}', fontsize=8, color='blue')
    if highlight_path:
        path_edges = list(zip(highlight_path[:-1], highlight_path[1:]))
        for loc1, loc2 in path_edges:
            x1, y1 = LOCATIONS[loc1]
            x2, y2 = LOCATIONS[loc2]
            plt.plot([x1, x2], [y1, y2], 'r-', linewidth=2)  # Highlight path in red

    # Display distance and price on the plot
    if distance is not None and price is not None:
        plt.text(0.5, 0.95, f'Distance: {distance} km, Price: ${price}', fontsize=12, ha='center', transform=plt.gca().transAxes)

    plt.title('Map of Locations, Hospitals, and Fire Stations')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.legend()
    plt.show()

