# Introduction
[![hugo-docs](https://github.com/williamyang98/oculink_m2_adapter/actions/workflows/hugo-deploy.yml/badge.svg)](https://github.com/williamyang98/oculink_m2_adapter/actions/workflows/hugo-deploy.yml)

Open source M.2 to Oculink adapter for the Lenovo Ideapad Pro 5 16ARP8 laptop. Includes a single board design and a flexible two board design.

Documentation on design, manufacturing and benchmarks can be found [here](https://williamyang98.github.io/oculink_m2_adapter/docs/)

## Single board design
![Single board Oculink adapter render](./docs/static/images/diagrams/kicad_single_board_render.png)
![Single board Oculink adapter](./docs/static/images/pictures/laptop_photo_single_board.jpg)

## Flexible two board design
![Flexible PCB multipart Oculink adapter render](./docs/static/images/diagrams/kicad_flex_connector_render.png)
![Flexible PCB multipart Oculink adapter](./docs/static/images/pictures/laptop_photo_flex_pcb.jpg)
![Flexible PCB multipart Oculink adapter](./docs/static/images/pictures/laptop_photo_flex_pcb_with_m2.jpg)

# Project guide
| Directory | Description |
| --- | --- |
| ```docs``` | Location of hugo docs which are published to [github pages](https://williamyang98.github.io/oculink_m2_adapter/docs/) |
| ```kicad``` | Location of KiCAD schematic and PCBs files |
| ```simuations``` | Location of openEMS Python simulations for parametric optimisation of transmission line hatched ground plane and tapers |
