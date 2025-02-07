---
title: Discussion
prev: /docs/results/synthetic_benchmarks
next: /docs/conclusion
weight: 3
---

## Display setup
```mermaid
sequenceDiagram;
    participant eGPU
    participant CPU
    participant USB 4 dock
    participant 1080p monitor
    CPU->>eGPU: Oculink PCIe TX
    eGPU->>CPU: Oculink PCIe RX
    CPU->>USB 4 dock: 40Gb/s USB 4 cable
    USB 4 dock->>1080p monitor: HDMI cable
```

- Benchmark output display is connected to a USB 4 dock (40Gb/s) and has a resolution of 1080p.
- This means Oculink PCIe connection has to be stable in both the transmit and receive direction.
- When eGPU data comes back to CPU it actually goes through the integrated AMD 680m based on copy activity in task manager.

## Flexible PCB and single board design
{{< carousel key="custom_adapters" >}}
<div class="carousel-item">
  <div class="responsive-image">
    <img src="{{< abs_url link=images/diagrams/kicad_single_board_render.png >}}" style="max-height: 200px">
  </div>
</div>
<div class="carousel-item">
  <div class="responsive-image">
    <img src="{{< abs_url link=images/diagrams/kicad_flex_connector_render.png >}}" style="max-height: 220px">
  </div>
</div>
{{< /carousel >}}

- Both the flexible PCB multi-board design and single board design achieved PCIe 3.0 speeds.
- Their results across all synthetic benchmarks were identical.
- PCIe 3.0 connection was stable and bandwidth reached theoretical values.
- PCIe 4.0 could not be achieved at all.

## Aliexpress PCIe 4.0 adapters
{{< carousel key="aliexpress_adapters" >}}
<div class="carousel-item">
  <div class="responsive-image">
    <img src="{{< abs_url link=images/diagrams/adtlink_f4c_m2_to_oculink_adapter_photo.png >}}">
  </div>
</div>
<div class="carousel-item">
  <div class="responsive-image">
    <img src="{{< abs_url link=images/diagrams/aliexpress_m2_oculink_pcie4_extension.png >}}" style="max-height: 220px">
  </div>
</div>
{{< /carousel >}}

- Both the adapters that came with the Adtlink eGPU and the silver plated 12cm adapter reached PCIe 4.0 speeds.
- PCIe 4.0 connection was stable and bandwidth reached theoretical values.
- Performance uplift from PCIe 3.0 to PCIe 4.0 in this setup is significant.
- Bandwidth limit from eGPU to CPU limits the number of frames that can be sent to display.
