########################################################################
### Filename    : proxy_iota_aba.sh
### Description : Turn on Shapes from the web - exec module proxy event from/to the web and the client
### Author      :  Marco Ercolani in data 25.01.2025
### A.A. 2024/2025
### Corso di Interaction Design 
### Scuola Nuove Tecnologie dell'Arte
### Accademia di Belle Arti di Urbino
### modification: 2025-01-25
########################################################################
## Run del proxy
## --address ercole.abaurbino.it 
## --port_client_socket 8182
## --port_client_websocket 8183
## --logging (console/<nome_file>) To view all messages for log
## --archive_client (Yes/No) Make an archive for all msg from client
## --archive_web (Yes/No) Make an archive for all msg from web
##
python3 proxy_iota_aba.py --address teseo.abaurbino.it --port_client_socket 11246 --port_client_websocket 11346 --logging proxy_iota_aba.log --archive_client No --archive_web No

