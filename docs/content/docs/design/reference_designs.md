---
title: Reference designs
prev: /docs/design/
next: /docs/design/laptop_measurements
weight: 1
params:
  icon: clipboard
---

- Both the M.2 and Oculink port have very similarly named PCIe pinouts.
- Oculink port pinout sometimes has TX and RX names swapped (PERxy/PETxy).
- Do you wire from PERxy on the M.2 side to PERxy on the Oculink side, or PERxy to PETxy?
- Is SMB (system management bus) data and clock required or is it optional?
- What about the MFG (manufacturer) data and clock on the M.2 card which is not present on the Oculink connector or PCIe standard?

## AdtLink M.2 to PCIe extension
{{< responsive_image key="adtlink_m2_to_pcie4_adapter_schematic" >}}
- {{< pdf_link key="adtlink_m2_pcie_x4_extension" >}}
- ```[CLKREQ, PERST]``` are connected.
- ```[PEWAKE, PEDET]``` are **not** connected.
- ```[SMB_CLOCK, SMB_DATA]``` are **not** connected.
- ```[MFG_CLOCK, MFG_DATA]``` are **not** connected.
- ```3.3V``` is connected.
- ```REFCLK``` is connected with same polarity.
- ```[PERxy, PETxy]``` lanes are connected with same polarity and same order.

## GPD Win v1 M.2 to Oculink card
{{< responsive_image key="gpdwin1_m2_to_oculink_adapter_schematic" >}}
- {{< pdf_link key="gpdwin1_schematic" >}}
- ```[PERST, PEDET]``` are connected.
- ```CLKREQ``` is connected but through a Schottky diode.
- ```PEWAKE``` is **not** connected.
- ```[SMB_CLOCK, SMB_DATA]``` are **not** connected.
- ```[MFG_CLOCK, MFG_DATA]``` are **not** connected.
- ```3.3V``` is connected through a jumper.
- ```REFCLK``` is connected with same polarity.
- ```[PERxy, PETxy]``` lanes are connected with same polarity and same order.

## Adtlink M.2 to Oculink card
{{< responsive_image key="adtlink_f4c_m2_to_oculink_adapter" >}}
{{< responsive_image key="adtlink_f4c_m2_to_oculink_adapter_photo" >}}
- {{< website_link key="adtlink_pcie4_egpu_dock" >}}
- ```[PERST, CLKREQ]``` are connected.
- ```[PEWAKE, PEDET]``` are **not** connected.
- ```[SMB_CLOCK, SMB_DATA]``` are connected.
- ```[MFG_CLOCK, MFG_DATA]``` are **not** connected.
- ```3.3V``` is connected.
- ```REFCLK``` is connected with same polarity.
- ```[PERxy, PETxy]``` lanes are connected with opposite polarity and opposite order.

## Summary
- ```PERST``` must be connected.
- ```CLKREQ``` must be connected, possibly through a diode, or shorted to ground on host side.
- ```PERST``` is optional.
- ```PEWAKE``` is not connected (might be optional?).
- ```[SMB_CLOCK, SMB_DATA]``` are optional.
- ```[MFG_CLOCK, MFG_DATA]``` are not connected.
- ```3.3V``` is connected.
- ```REFCLK``` must be connected with same polarity.
- ```[PERxy, PETxy]``` can be connected in opposite polarity and/or opposite order.
