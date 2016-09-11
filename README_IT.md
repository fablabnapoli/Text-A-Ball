# Project description.
Tweet A Ball (TaB) è una robot  ideato per riportare il testo dei tweet contenenti  specifici hashtags su palline, uova ed altre superfici sferiche.

A differenza delle altre EggBot e similari in circolazione, TaB è totalmente autonoma e non necessita di una stazione di controllo esterna (PC) o di software per l'elaborazione del testo da stampare. 

# Project history
TaB è stata realizzata dal Fablab Napoli nell'ambito dell'iniziativa IntelMaker in occasione della Maker Faire Rome 2016.

Il progetto, ideato principalmente con finalità didattiche, mira ad esplorare le potenzialità offerte dalla piattaforma Edison di Intel.

# Come funziona la TaB
Sfruttando le potenzialità di Intel Edison, la TaB può connettersi ad internet e scandagliare il flusso Twitter alla ricerca si specifici argomenti di discussione (hashtags).

Individuato un messaggio corrispondere ai criteri di ricerca, il software interno al robot lo converte in una serie di linee, curve e punti.

Infine il tutto viene convertito in una sequenza di comandi di movimento che attivano il braccio di scrittura.



# Software stack
Lo stack software è stato ideato specificamente per la piattaforma Intel Edison ed è costituito dei seguenti moduli:

* Dispatcher
* Host
* Post-processor
* Firmware

I moduli *Dispatcher*, *Host* e *Post-processor* sono stato stati concepiti in Python e vengono eseguiti dalla CPU,  mentre il modulo Firmware è stato adattato per la MCU di Intel Edison.


# Dispatcher
È il modulo che si occupa della selezione e del filtraggio dei tweets e della gestione dello spool (coda di stampa). 

## Host
Riceve il testo dal dispatcher, lo invia al post-processor per la conversione in istruzioni macchina (G-Code) e sovraintendente alla loro esecuzione inviando al Firmware un'istruzione alla volta.

## Post-processor
Traduce il testo fornitogli dall'Host in una sequenza di linee, curve e punti. Provvede poi alla conversione di queste ultime in istruzioni di movimento in G-Code.

## Firmware
É il core del sistema converte le istruzioni G-Code in impulsi elettrici ai motori e quindi in movimento del cursore di stampa e della pallina stessa

# TAB Network
Lo stack software interno è stato concepito in maniera tale da consentire che piu TaB robots collaborino nella rappresentazione dei tweet.

Ovvero un "network di TaB robots".

In questa configurazione una delle TaB assume il ruolo di master,  incaricandosi di selezionare i tweets da stampare e le altre agiscono come slave attendendo dalla prima i contenuti da rappresentare.

In una configurazione multi TaB un solo modulo Dispatcher sarà attivo in ogni momento è comunicherà tramite rete WiFi con diversi moduli Host dislocati su altre Intel Edison.

# Hardware stack

