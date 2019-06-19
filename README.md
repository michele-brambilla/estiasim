# estiasim
Simulation of the ESTIA device

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

