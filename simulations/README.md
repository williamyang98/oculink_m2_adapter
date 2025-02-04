# Introduction
- Simulation of PCB design using ```openEMS``` and ```gerber2ems```.
- Contains KiCAD schematics for:
    - Hatched ground planes in flexible PCBs.
    - Tapered differential pair for ground plane transitions.

# Setup
1. Clone ```gerber2ems``` submodule.
```bash
git submodule update --init --recursive
```

2. Create Python 3.10 virtual environment.
```bash
# create environment
python -m venv venv
# activate environment
source ./venv/Scripts/activate
```

3. Install gerber2ems. Refer to [gerber2ems repo](https://github.com/williamyang98/gerber2ems) for more details on setup and usage.
```bash
# install vendor binaries
./gerber2ems/vendor/download.sh
# add to binaries to path
source ./gerber2ems/vendor/update_path.sh
# install gerber2ems to virtual environment
pip install -e ./gerber2ems
```

# Environment activation and deactivation
```bash
# activate environment
source ./venv/Scripts/activate
# add vendor binaries to path
source ./gerber2ems/vendor/update_path.sh
# use gerber2ems
gerber2ems -h
# deactivate environment after usage
deactivate
```

# Instructions
Refer to simulation folders for detailed instructions on how to setup and run each setup.
