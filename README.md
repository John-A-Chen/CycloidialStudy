# Cycloidal Drive Maker (SolidWorks)

## Overview
This repository documents the design and development of a **cycloidal drive reduction mechanism** intended for compact, high-torque robotic and mechatronic applications.

The project focuses on **parametric CAD modelling in SolidWorks**, manufacturing-aware design, and clear engineering documentation rather than a single fixed geometry.

The aim is to provide a **well-engineered reference cycloidal drive**, suitable for learning, modification, and integration into custom actuators or robotic joints.

---

## Project Goals
- Develop a fully parametric cycloidal drive model in SolidWorks  
- Base geometry on correct cycloidal theory rather than approximations  
- Design with real manufacturing constraints in mind  
- Document assumptions, trade-offs, and design iterations  
- Produce drawings and files that can realistically be manufactured  

---

## What Is a Cycloidal Drive
A cycloidal drive is a high-reduction, low-backlash gearbox that uses an eccentrically driven cycloid disc engaging with a ring of pins.

Compared to conventional gear trains, cycloidal drives offer:
- High torque density  
- Good shock load resistance  
- Low backlash  
- Compact packaging  

These characteristics make them well suited to robotics, automation, and precision motion systems.

---

## Repository Structure
```

/Docs
/CAD
/Drawings

```

---

## Design Approach

### Parametric Modelling
All critical geometry (pin count, eccentricity, disc diameter, output bolt circle, etc.) is controlled through **SolidWorks global variables and equations**, allowing:
- Rapid ratio changes  
- Easy scaling  
- Clear traceability between calculations and CAD  

### Manufacturing-Aware Design
The design explicitly considers:
- Realistic tolerances  
- Bearing fits  
- Fastener access  
- Assembly order  
- CNC, laser-cut, and 3D-printed manufacturing paths  

This is not a purely theoretical model.

---

## Key Design Parameters (example)
> Update these as the design is finalised

- Reduction ratio: variable (function of pin count)  
- Cycloid discs: single or dual disc configuration  
- Input: eccentric shaft  
- Output: pinned carrier plate  
- Bearings: eccentric input bearing + output support bearing  
- Lubrication: grease-based  

---

## Tools Used
- SolidWorks (parametric CAD, assemblies, drawings)  
- Excel / hand calculations (geometry and load estimation)  
- GitHub for version control and documentation  

---

## Manufacturing Notes (High-Level)
- Cycloid disc profile accuracy is critical to smooth operation  
- Pin diameter tolerance directly affects backlash  
- Housing stiffness strongly influences bearing life  
- 3D printing is suitable for proof-of-concept, not final load testing  

Detailed notes are provided in the `Manufacturing_Notes` directory.

---

## Assembly and Testing
Assembly and testing procedures are documented to:
- Reduce preload and misalignment  
- Ensure repeatable results  
- Allow basic efficiency and backlash measurements  

This includes exploded views, assembly order, and inspection points.

---

## Limitations and Future Work
**Current limitations**
- No hardened steel components in the initial version  
- No experimental torque testing yet  
- Efficiency currently estimated analytically  

**Planned future work**
- Load testing  
- Backlash measurement  
- Alternative disc profiles  
- Integrated motor mount  
- Comparison against harmonic drives  

---

## References
- Cycloidal Drive – Wikipedia  
  https://en.wikipedia.org/wiki/Cycloidal_drive  

- MIT cycloidal drive notes  
  https://fab.cba.mit.edu/classes/MIT/863.15/people/jonas/cycloidal_drive.pdf  

- Nabtesco motion control (industry reference)  
  https://www.nabtesco-motioncontrol.com  

- SKF bearing engineering resources  
  https://www.skf.com  

---

## Licence
This project is licensed under the **MIT License**.  
You are free to use, modify, and adapt the designs with attribution.

---

## Author
**John Chen**  
Mechatronics Engineering (UTS)  
Focus areas: mechanical design, robotics, CAD-driven engineering systems
