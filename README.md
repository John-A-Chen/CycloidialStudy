# Cycloidal Drive Maker (SolidWorks)

## Overview
This repository documents the design and development of a **cycloidal drive reduction mechanism** intended for compact, high-torque robotic and mechatronic applications. This is not a new field, but I found it cool so I wanted to make my own stuff by drawing from several existing repositories for inspiration.

The project focuses on **parametric CAD modelling in SolidWorks**, manufacturing-aware design, and clear engineering documentation rather than a single fixed geometry. Most existing tools are for other CAD softwares, so I wanted to see if there could be a better method for SolidWorks.

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
A cycloidal drive is a high-reduction, low-backlash gearbox that uses an eccentrically driven cycloid disc engaging with a ring of pins. Compared to conventional gear trains, cycloidal drives offer:
- High torque density  
- Good shock load resistance  
- Low backlash  
- Compact packaging  

---

## Repository Structure
```
/App
/CAD
/Docs
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

I plan on printing these drives on my BambuLab P1s and may try to include printer profiles since some slicers already have per-printer tuning. 
---

## Tools Used
- SolidWorks (parametric CAD, assemblies, drawings)  
- Excel / hand calculations (geometry and load estimation)  
- GitHub for version control and documentation  

Detailed notes are provided in the `Docs` directory.

---

## Assembly and Testing
Assembly and testing procedures are documented to:
- Reduce preload and misalignment  
- Ensure repeatable results  
- Allow basic efficiency and backlash measurements  

This includes exploded views, assembly order, and inspection points to the best of my abilities.

Planned future work includes:
- Load testing  
- Backlash measurement  
- Alternative disc profiles  
- Integrated motor mount  
- Comparison against harmonic drives  

---

## References

Wikipedia
Cycloidal drive. Wikipedia, The Free Encyclopedia.
https://en.wikipedia.org/wiki/Cycloidal_drive

Qi, L., Yang, D., Cao, B., Li, Z., Liu, H. (2024).
Design principle and numerical analysis for cycloidal drive considering clearance, deformation, and friction.
Alexandria Engineering Journal, Volume 91, Pages 403–418.
https://doi.org/10.1016/j.aej.2024.01.077

Shimpo Drive Systems
Circulute series cycloidal speed reducers – operating principles and structure.
Shimpo / Nidec-Shimpo technical catalogue.

Sensinger, J. W., & Lipsey, J. H. (2012).
Cycloid vs. harmonic drives for use in high ratio, single stage robotic transmissions.
Proceedings of the IEEE International Conference on Robotics and Automation (ICRA).

Johnson, K. L. (1985).
Contact Mechanics.
Cambridge University Press.

Radzevich, S. P. (2018).
Theory of Gearing: Kinematics, Geometry, and Synthesis (2nd ed.).
CRC Press, Taylor & Francis Group.

Nabtesco Motion Control
RV reducer technical principles and application notes.
https://www.nabtesco-motioncontrol.com

Suarez, D. (n.d.). GearSolver (GitHub repository). https://github.com/dsuarezv/GearSolver

Younis, O. (n.d.). cycloidal_drive_creator (GitHub repository). https://github.com/osyounis/cycloidal_drive_creator

skavrx. (n.d.). cycloidal-drive-v1 (GitHub repository). https://github.com/skavrx/cycloidal-drive-v1

SakethGG. (n.d.). Cycloidal-Drive-Design (GitHub repository). https://github.com/SakethGG/Cycloidal-Drive-Design

drewim. (n.d.). cycloidal_drive (GitHub repository). https://github.com/drewim/cycloidal_drive

woodenCaliper. (n.d.). CycloidalDrive (GitHub repository). https://github.com/woodenCaliper/CycloidalDrive

iplayfast. (n.d.). CycloidGearBox (GitHub repository). https://github.com/iplayfast/CycloidGearBox


---

## Licence
This project is licensed under the **MIT License**.  
You are free to use, modify, and adapt the designs with attribution.

---

## Author
**John Chen**  
Mechatronics Engineering (UTS)  
Focus areas: mechanical design, robotics, CAD-driven engineering systems
