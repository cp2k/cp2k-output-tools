"""
Convert the CP2K band structure output to CSV files
"""

import argparse
from os import path

from cp2k_output_tools.bandstructure_parser import set_gen


def cp2k_bs2csv():
    parser = argparse.ArgumentParser(
        description="""
    Convert the input from the given input file handle and write
    CSV output files based on the given pattern.
    """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "bsfile", metavar="<bandstructure-file>", type=argparse.FileType("r"), help="the band structure file generated by CP2K"
    )
    parser.add_argument(
        "-p", "--output-pattern", help="The output pattern for the different set files", default="{bsfile_basename}.set-{setnr}.csv"
    )
    args = parser.parse_args()

    content = args.bsfile.read()

    for setnr, totalpoints, _, specialpoints, points in set_gen(content):
        filename = args.output_pattern.format(bsfile_basename=path.basename(args.bsfile.name), setnr=setnr)

        print(f"writing point set {filename} (total number of k-points: {totalpoints})")
        with open(filename, "w") as csvout:
            print("with the following special points:")

            for point in specialpoints:
                print(f"  {point.name:>8}: {point.a:10.8f} / {point.b:10.8f} / {point.c:10.8f}")

            for point in points:
                csvout.write(f"{point.a:10.8f} {point.b:10.8f} {point.c:10.8f}")
                for value in point.bands:
                    csvout.write(f" {value:10.8f}")
                csvout.write("\n")
