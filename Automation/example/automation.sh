#!/bin/bash

scale="$1"

if [[ -z $scale ]]; then
    scale="0.05"
fi

echo "Running simulation"
./simulation.py --scale $scale

echo "Rendering result image"
pvbatch render_state.py

echo "Creating plot data"
pvbatch make_plot_data.py

echo "Making plot image"
python3 plot.py
