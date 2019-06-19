FROM dmscid/epics-base:latest

ENV EPICS_BASE=/EPICS/base
ENV EPICS_HOST_ARCH=linux-x86_64

RUN apk update &&\
    apk --no-cache add git python3 python3-dev curl binutils swig gcc g++&&\
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py &&\
    python3 get-pip.py && \
    git clone https://github.com/michele-brambilla/estiasim.git &&\
    pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir -r /estiasim/pcaspysim/requirements.txt

WORKDIR /estiasim/pcaspysim

ENV MOTORS "m1 m2"
ENV SIMDEVICE "cart"
CMD python3 "$SIMDEVICE"sim.py -m $MOTORS
