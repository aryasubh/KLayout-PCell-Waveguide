# scripts/waveguide_pcell.py
# Author: Subhash C Arya, LWCS Laboratory, Department of ECE, NEHU
# Description: Simple waveguide PCell for KLayout using SiEPIC-Tools

import pya
import SiEPIC
from SiEPIC.utils import get_technology_by_name

class WaveguidePCell(pya.PCellDeclarationHelper):
    """
    Straight Waveguide PCell for SiEPIC EBeam PDK
    Author: Subhash Arya (updated with fixes)
    """
    def __init__(self):
        super().__init__()
        self.param("width", self.TypeDouble, "Waveguide Width (um)", default=0.5)
        self.param("length", self.TypeDouble, "Waveguide Length (um)", default=10.0)

    def produce_impl(self):
        # Get EBeam technology layers
        try:
            tech = get_technology_by_name("EBeam")
        except:
            # Fallback layer indices (adjust if your technology uses different numbers)
            tech = {
                "Si": self.layout.layer(1, 0),
                "DevRec": self.layout.layer(68, 0),
                "PinRec": self.layout.layer(69, 0)
            }

        width = self.width
        length = self.length

        # === Silicon Waveguide Core ===
        points = [
            pya.DPoint(0, -width / 2.0),
            pya.DPoint(length, -width / 2.0),
            pya.DPoint(length, width / 2.0),
            pya.DPoint(0, width / 2.0)
        ]
        wg_poly = pya.DPolygon(points)
        self.cell.shapes(tech["Si"]).insert(wg_poly)

        # === Device Recognition (DevRec) ===
        devrec_box = pya.DBox(0, -width / 2.0, length, width / 2.0)
        self.cell.shapes(tech["DevRec"]).insert(devrec_box)

        # === Pin Recognition (PinRec) ===
        pinrec = tech["PinRec"]
        pin_len = 0.2   # µm (standard in SiEPIC)
        half_pin = pin_len / 2.0

        # Left Pin
        self.cell.shapes(pinrec).insert(pya.DBox(-half_pin, -width/2.0, half_pin, width/2.0))
        # Right Pin
        self.cell.shapes(pinrec).insert(pya.DBox(length - half_pin, -width/2.0, length + half_pin, width/2.0))

        # === Pin Labels (Critical for SiEPIC netlisting) ===
        text_size = 0.4  # µm

        # Left pin text
        t1 = pya.DText("pin1", pya.DPoint(0, 0), text_size)
        t1.halign = pya.DText.HAlignCenter
        t1.valign = pya.DText.VAlignCenter
        self.cell.shapes(pinrec).insert(t1)

        # Right pin text
        t2 = pya.DText("pin2", pya.DPoint(length, 0), text_size)
        t2.halign = pya.DText.HAlignCenter
        t2.valign = pya.DText.VAlignCenter
        self.cell.shapes(pinrec).insert(t2)


# ==================== Library Registration ====================
class WaveguideLibrary(pya.Library):
    def __init__(self):
        self.description = "Custom Straight Waveguide PCell for SiEPIC EBeam"
        self.layout().register_pcell("Waveguide", WaveguidePCell())
        self.register("WaveguideLibrary")

# Create the library when macro is run
WaveguideLibrary()