# Simple Fusion Systems Code

Simple fusion reactor systems code, based on the approach in Plasma Physics and Fusion Energy, Freidberg  
Section 5.5  
Adapted and expanded by Richard Kembleton for TU/e Fusion Reactor Design Masterclass  
2021  
Additional plasma equations from Iter Physics Design Guidelines 1989 (Uckan)  
and Iter Physics Basis Nucl. Fusion 39 (1999)  
Radiation equations from  
Matthews et al, Nuc. Fus. 39 (1999)  
Johner, Fus. Sci. Tech. 59 (2011)  
Uckan (1989)  

## How to install this script (on Linux):
1. Clone repository

git clone pulls the project.  
`git clone https://github.com/IPP-SRS/simple-fusion-systems-code.git`  

cd enters working folder.  
`cd simple-fusion-systems-code-main`

2. Create Python virtual environment (in VS Code, you can also make it with ctrl+shift+P)  

`python3 -m venv .venv`  
`source .venv/bin/activate`

3. Update pip + install requirements

`pip install --upgrade pip`  
`pip install -r requirements.txt`

## Important content

run_analysis.py - script for analysis execution  
simplesystemcode.py - system code backend  

