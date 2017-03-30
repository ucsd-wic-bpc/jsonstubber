#!/bin/bash

cd ..

for sample in ${PWD}/jsonstubber/samples/problem*.py; do
  module=${sample##*/}
  module=${module%*.py}

  python -m jsonstubber.samples.$module
done
