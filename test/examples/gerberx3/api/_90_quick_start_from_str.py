from pygerber.gerber.api import GerberFile

source_code = """
%FSLAX26Y26*%
%MOMM*%
%ADD100C,1.5*%
D100*
X0Y0D03*
M02*
"""

gerber_file = GerberFile.from_str(source_code)
