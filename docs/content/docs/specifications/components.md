---
title: M.2 to Oculink
prev: /docs/specifications/pcie_specification
next: /docs/design
weight: 2
params:
  icon: chip
---

## M.2 card
- Usually used for M.2 SSDs in laptop or desktop motherboards.
- Pins follow the PCIe specification for x4 lanes.

{{< responsive_image key="m2_card_size" style="width: 75%" >}}
{{< responsive_image key="m2_connector_pinout_table" style="width: 50%" >}}

## Oculink port
- Follows the SFF-9402 specification which is compatible with PCIe
- {{< pdf_link key="sff_9402_specification" >}}
- Female port is rated for 10000 insertion cycles.
- Male cable is rated at a minimum of 50.
- Compatible with the PCIe specification for x4 or x8 lanes.
- Wider x8 lane variant is not as useful since no M.2 slot as of yet supports PCIe x8 lanes.
- {{< pdf_link key="amphenol_oculink_port_datasheet" >}}

{{< responsive_image key="amphenol_oculink_port" style="width: 50%" >}}
{{< responsive_image key="amphenol_oculink_port_pinout_table" >}}
