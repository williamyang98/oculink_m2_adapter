---
title: Synthetic benchmarks
prev: /docs/results/gpu_bandwidth
next: /docs/conclusion
weight: 2
---

## Custom adapter compared to Aliexpress PCIe 4.0 rated adapter
- Half the PCIe bandwidth resulted in degraded performance
- Usually occured on benchmarks with high FPS numbers where PCIe link would be used more
- Aliexpress PCIe 4.0 adapter achieved higher scores on average
- Performance penalty when monitor output has to go back through eGPU oculink connection and through iGPU to external display
    - Setup was CPU -> eGPU -> iGPU -> USB 4 dock -> Monitor
