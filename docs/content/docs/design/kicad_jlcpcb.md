---
title: KiCAD & JLCPCB
prev: /docs/design/laptop_measurements
next: /docs/design/single_board
weight: 3
params:
  icon: calculator
---

## Reasons to use KiCAD
- Free and open source. No license required for usage.
- More than adequate for passive M.2 to Oculink adapter.
- Transmission line calculators are limited but there are plenty of more capable free and public options.
- Lacks high end simulation capabilities like Altium but open source substitutes are available.

## Reasons to use JLCPCB
- The cheapest PCB manufacturer.
- Offers plenty of discounts for extremely low prices.
- If you stay under certain size requirements the cost will remain exceptionally low.
- Inexpensive 0.8mm thick stackup which is required for M.2 edge connector.
    - Only requires lead free HASL to be the mandatory surface finish which costs $4.80USD.
- Inexpensive board cost if certain size thresholds aren't exceeded.
    - For boards less than 50mm x 50mm board cost is only $2.00USD.
    - For boards between 50mm x 50mm and 100mm x 100mm the board cost is $7.00USD.
    - For boards above 100mm x 100mm there is an aditional engineering fee which costs $24.00USD.
- Inexpensive 4 layer boards which are important for maintaining solid ground plane if signal traces need to be routed on separate layers.
- Controlled impedance stackup to meet transmission line design requirements.
- Allows choosing denser more uniform fibre weaves to improve signal integrity in transmission lines.
    - A non-uniform weave could cause problems if a differential trace were routed over it.
    - Each side of the pair could be on a piece of the weave with different densities of fibres.
    - This would mean each trace in the pair experiences a different dielectric constant.
    - Since the speed of propagation is dependent on the dielectric constant, a skew in the time domain would be induced in the differential pair.
    - PCIe standard has relatively 
- ENIG (gold plating) to prevent oxidation of M.2 edge connector and flatter profile for more reliable reflow soldering.
- Flexible PCBs for designs that require large amounts of vertical routing.
- Very generous constraints minimum via sizes and pad pitch which is important for high frequency design where physical dimensions of traces, vias, and connector pitch can get very small.

## Importing design constraints into KiCAD
- JLCPCB specifies manufacturing capabilities.
- {{< website_link key="jlcpcb_manufacturing_capabilities" >}}
- The values for certain constraints will vary depending on options you select for the number of layers, minimum via size and stackup type.
- KiCAD supports creating a design rules file to automatically check these manufacturing constraints to prevent submitting unmanufacturable designs to a fabricator.
- The design rules checker (DRC) can be triggered manually or is run automatically before generating gerber and drill files.
- {{< website_link key="kicad_drc_file_example" >}}

## Generating gerber and drill files
- Gerber and drill files must match what the fabricator expects.
- JLCPCB specifies instructions for KiCAD 7.0 as well as other versions.
- {{< pdf_link key="jlcpcb_kicad_7_generate_gerber_and_drill_files" >}}
- Verify output through local gerber viewer program before submitting.
- Final verification in JLCPCB online gerber viewer after uploading design.
