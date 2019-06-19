# estiasim
Simulation of the ESTIA device

Two different simulations are available, corresponding to the two main 
folders, based on  PCASPY and [LeWIS](https://github.com/ess-dmsc/lewis 
"LeWIS's Homepage").

## LeWIS
Run it with
```bash
lewis -a /home/estiasim -k lewissim estia -p epics --adapter-options "epics:
 {prefix: 'PSI-ESTIARNS:MC-MCU-01:<motorname>.'}"
```
 
 Unfortunately one simulation can only deal with one motor (so far).


##PCASPY

```bash
python cartsim.py -m <list of motor names> 

```

## EPICS PVs

The EPICS PV prefix is 
```bash
PSI-ESTIARND:MC-MCU-01:<motor name>
```

## Using the Docker container

The simulation can be run in a docker container:

```bash
docker run --rm -it -e MOTORS='m11 m12' -e SIMDEVICE='selene' mbrambilla/estiasim:pcaspy
```

Two environment variables allows to configure the simulation:
- 'MOTORS' select the name of the motors
- 'SIMDEVICE' allows to simulate either the **metronomy cart** (` -e 
SIMDEVICE='cart'`) or the **selene alignment system** (`-e SIMDEVICE='selene'`) 

