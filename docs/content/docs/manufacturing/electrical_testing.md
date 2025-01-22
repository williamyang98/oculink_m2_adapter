---
title: Electrical Testing
prev: /docs/manufacturing/reflow_soldering
next: /docs/results
weight: 3
params:
  icon: badge-check
---

## Checking for shorts
- Oculink port after reflow can be shorted due to excess or smeared solder paste resulting in bridges between fine pitch pins
    - Can redo reflow as many times until short is gone
- For flex pcb shorts can occur between fine pitch SMD pads of FFC connector
    - Visual inspection through transparent FFC can reveal where shorts are

## Checking flex pcb during assembly
- For flex pcb bad connections can be checked partially through assembly
- Begin by soldering FFC to M.2 card
    - Check for shorts and bad connections between M.2 edge connector and end of FFC cable
- Begin reflowing oculink port to separate PCB
    - Check for shorts on exposed connector pads
- Bad connection or short will likely be located at FFC to oculink board connection

## Checking assembled board 
- Connect oculink adapter to eGPU board
- The PCIe connector on the eGPU board can be used to check for continuity and shorts
    - Refer to following schematic for pin out of PCIe connector
- Use m.2 edge connector as other side of connection
    - Refer to pinout for m.2 connector



