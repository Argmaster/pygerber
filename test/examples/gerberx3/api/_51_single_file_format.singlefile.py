from pygerber.gerber.api import GerberFile, Options

source_code = """
%FSLAX26Y26*%%MOMM*%%ADD100C,1.5*%D100*X0Y0D03*M02*
"""

gerber_file = GerberFile.from_str(source_code)
formatted_code = gerber_file.formats(Options(d03_indent=2))

print(formatted_code)
