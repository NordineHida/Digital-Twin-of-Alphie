"""
File:          NetworkManager.py
Date:          February 2024
Description:   Create and organise a Mesh network between robots.
               You can find more information about this network here :
               https://howtomechatronics.com/tutorials/arduino/how-to-build-an-arduino-wireless-network-with-multiple-nrf24l01-modules/
Author:        Nordine HIDA
Modifications:
"""

class NetworkManager:
    def __init__(self):
        self.network = {}  # Dictionary to store network topology

    def create_mesh_network(self, num_robots):
        # Create a mesh network among the given number of robots
        # Each robot is identified by its name


        # Organize the mesh network topology (e.g., tree topology)
        # Assuming a simple tree topology where each robot has one parent except the root
        for i in range(2, num_robots + 1):
            robot_name = f"Robot{i}"
            parent_name = f"Robot{i // 2}"
            self.add_neighbor(parent_name, robot_name)

    def get_network_topology(self):
        # Return the current network topology
        return self.network

    def add_neighbor(self, robot_name, neighbor_name):
        # Add a neighbor to the specified robot in the network
        if robot_name in self.network:
            self.network[robot_name].append(neighbor_name)

    def remove_neighbor(self, robot_name, neighbor_name):
        # Remove a neighbor from the specified robot in the network
        if robot_name in self.network:
            if neighbor_name in self.network[robot_name]:
                self.network[robot_name].remove(neighbor_name)
