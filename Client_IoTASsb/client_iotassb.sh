#!/bin/bash
########################################################################
# Filename    : client_iotassb.sh
# Project IoTA Swarm Scribble Bots
# Description : Activation Scribble Bot with input commands that arrive from Internet
# Author      : Marco Ercolani in data 01.02.2025
# A.A. 2024/2025
# Corso di Interaction Design 
# Scuola Nuove Tecnologie dell'Arte
# Accademia di Belle Arti di Urbino
# modification: 2024-12-18
########################################################################
### Batch File to run client IoTASsb on system Linux/Mac
### Use syntax
###--address ADDRESS --port_client_socket PORT_CLIENT_SOCKET
### example - python3 client_iotageneric.py --address teseo.abaurbino.it --port_client_socket 8182
python3 client_iotassb.py --address teseo.abaurbino.it --port_client_socket 11263

