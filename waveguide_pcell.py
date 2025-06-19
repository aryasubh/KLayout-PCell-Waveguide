# scripts/waveguide_pcell.py
# Author: Subhash C Arya, LWCS Laboratory, Department of ECE, NEHU
# Description: Simple waveguide PCell for KLayout using SiEPIC-Tools

import pya
import SiEPIC
from SiEPIC.utils import get_technology_by_name

class WaveguidePCell(pya.PCellDeclarationHelper):
    def __init__(self):
        super().__init__()
        self.param("width", self.TypeDouble, "Waveguide Width (um)", default=0.5)
        self.param("length", self.TypeDouble, "Waveguide Length (um)", default=10.0)

    def display_text_impl(self):
        return f"Waveguide (width={self.width}, length={self.length})"

    def produce_impl(self):
        tech = get_technology_by_name("EBeam")
        dbu = self.layout.dbu
        width = self.width / dbu
        length = self.length / dbu
        points = [
            pya.DPoint(0, -width/2),
            pya.DPoint(length, -width/2),
            pya.DPoint(length, width/2),
            pya.DPoint(0, width/2)
        ]
        shape = pya.DPolygon(points)
        self.cell.shapes(self.layout.layer(tech["Si"])).insert(shape)

# Register the PCell
class WaveguideLibrary(pya.Library):
    def __init__(self):
        self.description = "Waveguide PCell Library"
        self.layout().register_pcell("Waveguide", WaveguidePCell())
        self.register("WaveguideLibrary")

WaveguideLibrary()
