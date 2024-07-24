from vpython import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import json

class CreateMoleculeModel:
    def __init__(self):
        self.covalent_radii = {}
        self.atomic_masses = {}
        self.cpk_hex_colors = {}

        self.atoms = []
        self.connectivity = []

        self.get_elements_data_from_json()

        Tk().withdraw()
        self.xyz_filename = askopenfilename(title="Select .xyz file with your molecule", filetypes=[("XYZ files", "*")])

        self.get_atoms_positions_from_file(self.xyz_filename)
        self.get_connectivity()

    def get_elements_data_from_json(self):
        with open('elements_data.json', 'r') as json_file:
            json_object = json.load(json_file)
        
        for elem in json_object['elements']:
            symbol = elem['symbol']
            mass = elem['atomic_mass']
            covalent_radius = elem['covalent_radius']
            cpk_hex = elem['cpk_hex']
            cpk_hex = tuple(int(cpk_hex[i:i+2], 16) / 255.0 for i in (0, 2, 4))

            self.atomic_masses[symbol] = mass
            self.cpk_hex_colors[symbol] = vector(cpk_hex[0], cpk_hex[1], cpk_hex[2])

            if covalent_radius != "N/A":
                self.covalent_radii[symbol] = float(covalent_radius) * 1.08

    def get_atoms_positions_from_file(self, xyz_filename):
        with open(xyz_filename) as file:
            for line in file:
                if len(line.split()) >= 4:
                    elems = line.split()

                    atom_symbol = elems[-4]

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
                    self.connectivity.append([atom_1[0], atom_2[0] - atom_1[0], dist / 2.0, self.cpk_hex_colors[atom_1[1]]])

                    self.connectivity.append([atom_2[0], atom_1[0] - atom_2[0], dist / 2.0, self.cpk_hex_colors[atom_2[1]]])        

    def draw_molecule(self):
        canvas(title=self.xyz_filename, width=1000, height=600, caption= '''
            To rotate "camera", drag with right button or Ctrl-drag.
            To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
            To pan left/right and up/down, Shift-drag.
        ''')

        for atom in self.atoms:
                sphere(pos=atom[0], radius=0.1 * self.atomic_masses[atom[1]] ** 0.25, color=self.cpk_hex_colors[atom[1]])

        for edge in self.connectivity:
                cylinder(pos=edge[0], axis=edge[1], length=edge[2], radius=0.05, color = edge[3])

        # drawing vector:            
        # arrow(pos=vector(0, 0, 0), axis=vector(1, 0, 0), color=color.red)

          
visualizator = CreateMoleculeModel()

visualizator.draw_molecule()

while True:
    pass