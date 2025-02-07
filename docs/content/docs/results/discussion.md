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
- Both the flexible PCB multi-board design and single board design achieved PCIe 3.0 speeds.
- Their results across all synthetic benchmarks were identical.
- PCIe 3.0 connection was stable and bandwidth reached theoretical values.
- PCIe 4.0 could not be achieved at all.

## Aliexpress PCIe 4.0 adapter
- PCIe 4.0 connection was stable and bandwidth reached theoretical values.
- Performance uplift from PCIe 3.0 to PCIe 4.0 in this setup is significant.
- Bandwidth limit from eGPU to CPU limits the number of frames that can be sent to display.
