#!/usr/bin/env bash

$(rm -rf Pydocs)
$(mkdir Pydocs)
pydoc -w utilities triangulations sub_triangle_property triangle_property initialization main state_manipulation debugging error_checking state_tracking simulation move_factory
$(mv *.html Pydocs)

cd moves
pydoc -w AlexanderMove InverseAlexanderMove PinchingMove Move CollapseMove
$(mv *.html ../Pydocs)
