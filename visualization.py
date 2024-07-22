from vpython import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import random
import hashlib
import json

class CreateMoleculeModel:
    def __init__(self):
        self.covalent_radii = {}
        self.atomic_masses = {}
        self.colors_dict = {}

        self.atoms = []
        self.connectivity = []

        self.get_elements_data_from_json()

        Tk().withdraw()
        xyz_filename = askopenfilename(title="Select .xyz file with your molecule", filetypes=[("XYZ files", "*.xyz")])

        self.get_atoms_positions_from_file(xyz_filename)
        self.get_connectivity()
   
    def random_color(self, string, int): 
        h = hash( string + str(int) )
        
        if h < 0:
            h = h * -1
        
        random.seed(h)
        
        output = random.random()
        output = round(output, 6)
        
        return output


    def get_elements_data_from_json(self):
        with open('elements_data.json', 'r') as json_file:
            json_object = json.load(json_file)
        
        for elem in json_object['elements']:
            symbol = elem['symbol']
            mass = elem['atomic_mass']
            covalent_radius = elem['covalent_radius']

            self.atomic_masses[symbol] = mass

            if covalent_radius != "N/A":
                self.covalent_radii[symbol] = float(covalent_radius) * 1.08

    def get_atoms_positions_from_file(self, xyz_filename):
        with open(xyz_filename) as file:
            for line in file:
                if len(line.split()) >= 4:
                    elems = line.split()

                    atom_symbol = elems[-4]

                    if atom_symbol not in self.colors_dict:
                        color = vector(self.random_color(atom_symbol, 0), self.random_color(atom_symbol, 1), self.random_color(atom_symbol, 2))
                        self.colors_dict[atom_symbol] = color
                    
                    x_coord = float(elems[-3])
                    y_coord = float(elems[-2])
                    z_coord = float(elems[-1])

                    self.atoms.append([vector(x_coord, y_coord, z_coord), atom_symbol])

    def get_connectivity(self):
        for i in range(len(self.atoms)):
            for j in range(i+1, len(self.atoms)):
                atom_1 = self.atoms[i]
                atom_2 = self.atoms[j]

                if atom_1[1] not in self.covalent_radii:
                    raise Exception("Covalent radius of atom " + atom_1[1] + " not found in elements_data.json") 
                if atom_2[1] not in self.covalent_radii:
                    raise Exception("Covalent radius of atom " + atom_2[1] + " not found in elements_data.json") 

                dist = mag(atom_1[0] - atom_2[0])

                if dist <= self.covalent_radii[atom_1[1]] + self.covalent_radii[atom_2[1]]:
                    self.connectivity.append([atom_1[0], atom_2[0] - atom_1[0], dist])

    def draw_molecule(self):
        scene.caption= '''
            To rotate "camera", drag with right button or Ctrl-drag.
            To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
            To pan left/right and up/down, Shift-drag.
        '''

        while True:
            rate(60)

            for atom in self.atoms:
                sphere(pos=atom[0], radius=0.1 * self.atomic_masses[atom[1]] ** 0.5, color=self.colors_dict[atom[1]])

            for edge in self.connectivity:
                cylinder(pos=edge[0], axis=edge[1], length=edge[2], radius=0.05)

visualizator = CreateMoleculeModel()

visualizator.draw_molecule()