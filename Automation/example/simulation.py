#!/usr/bin/env python3

from typing import Tuple, List
from math import sin, cos, pi
from dataclasses import dataclass
from textwrap import dedent
from argparse import ArgumentParser

@dataclass
class Raster:
    size_x: int
    size_y: int
    x0: float
    y0: float
    dx: float
    dy: float


Point = Tuple[float, float]
def function(x: Point, scale: float) -> float:
    base_frequency = 10.0*pi/180.0
    num_overtones = 5

    lat = x[0]*180.0/pi
    lon = x[1]*180.0/pi

    result = 0.0
    for i in range(num_overtones):
        overtone_frequency = base_frequency*(i + 1)
        offset = i*base_frequency*pi/4.0
        if i % 2 == 0:
            result += scale*sin(overtone_frequency*(lat - offset))
            result += scale*cos(overtone_frequency*(lon - offset))
        else:
            result += scale*cos(overtone_frequency*(lat - offset))
            result += scale*sin(overtone_frequency*(lon - offset))
    return result*(lat*pi/180.0 + lon*pi/180.0)


def write_vts(filename: str, raster: Raster, point_data: Tuple[str, List[float]]) -> None:
    x1 = raster.x0 + raster.size_x*raster.dx
    y1 = raster.y0 + raster.size_y*raster.dy
    with open(filename + ".vti", "w") as vti_file:
        vti_file.write(dedent(f'''
            <VTKFile type="ImageData">
              <ImageData WholeExtent="0 {raster.size_x} 0 {raster.size_y} 0 0"
                         Origin="{raster.x0} {raster.y0} 0"
                         Spacing="{raster.dx} {raster.dy} 0">
                <Piece Extent="0 {raster.size_x} 0 {raster.size_y} 0 0">
                  <PointData>
                    <DataArray NumberOfComponents="1" type="Float64" Name="{point_data[0]}">
        '''))
        vti_file.write(" ".join((str(v) for v in point_data[1])))
        vti_file.write(dedent('''
                    </DataArray>
                  </PointData>
                </Piece>
              </ImageData>
            </VTKFile>
        '''))


def simulate(scale: float) -> None:
    size_x = 1.0
    size_y = 1.0
    num_cells_per_axis = 250
    num_points_per_axis = num_cells_per_axis + 1
    dx = size_x/num_cells_per_axis
    dy = size_y/num_cells_per_axis
    x0 = -0.5*size_x
    y0 = -0.5*size_y

    function_values = [
        function((x0 + float(i)*dx, y0 + float(j)*dy), scale)
        for i in range(num_points_per_axis)
        for j in range(num_points_per_axis)
    ]

    write_vts(
        "result",
        Raster(
            size_x=num_cells_per_axis,
            size_y=num_cells_per_axis,
            x0=x0,
            y0=y0,
            dx=dx,
            dy=dy
        ),
        ("function", function_values)
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-s", "--scale", required=False, default=0.05, type=float)
    args = vars(parser.parse_args())
    simulate(args["scale"])
