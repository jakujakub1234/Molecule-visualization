from vpython import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import random
import hashlib

class CreateMoleculeModel:
    def __init__(self):
        self.covalent_radii = {}
        self.colors_dict = {}

        self.atoms = []
        self.connectivity = []

        self.get_covalent_radii_dict()

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


    def get_covalent_radii_dict(self):
        with open("covalent_radii_data.txt") as file:
            for line in file:
                if len(line.split()) == 2:
                    symbol, radius = line.split()
                    self.covalent_radii[symbol] = float(radius)

    def get_atoms_positions_from_file(self, xyz_filename):
        with open(xyz_filename) as file:
            for line in file:
                if len(line.split()) >= 4:
                    elems = line.split()

                    atom_symbol = elems[-4]

                    if atom_symbol in self.colors_dict:
                        color = self.colors_dict[atom_symbol]
                    else:
                        color = vector(self.random_color(atom_symbol, 0), self.random_color(atom_symbol, 1), self.random_color(atom_symbol, 2))
                        self.colors_dict[atom_symbol] = color
                    
                    x_coord = float(elems[-3])
                    y_coord = float(elems[-2])
                    z_coord = float(elems[-1])

                    self.atoms.append([vector(x_coord, y_coord, z_coord), color, atom_symbol])

    def get_connectivity(self):
        for i in range(len(self.atoms)):
            for j in range(i+1, len(self.atoms)):
                atom_1 = self.atoms[i]
                atom_2 = self.atoms[j]

                if atom_1[2] not in self.covalent_radii:
                    raise Exception("Atom " + atom_1[2] + " not found in covalent_radii_data.txt") 
                if atom_2[2] not in self.covalent_radii:
                    raise Exception("Atom " + atom_2[2] + " not found in covalent_radii_data.txt") 

                dist = mag(atom_1[0] - atom_2[0])

                if dist - 0.2 <= self.covalent_radii[atom_1[2]] + self.covalent_radii[atom_2[2]]:
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
                sphere(pos=atom[0], radius=0.1, color=atom[1])

            for edge in self.connectivity:
                cylinder(pos=edge[0], axis=edge[1], length=edge[2], radius=0.05)

visualizator = CreateMoleculeModel()

visualizator.draw_molecule()