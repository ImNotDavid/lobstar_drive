# Drive board command documentation
The drive board is connected via usb serial at /dev/ttyUSB0 Baud rate 115200, no parity, no hardware flow control, 1 stop bit.

## Commands 
The important commands are:

`$spd:0,0,0,0#`
Control the speed of 4 motors	Example: $spd:100,-100,0,50#	Control the speed of 4 motors M1:100 M2:-100 M3:0 M4:50.

In our case, the forward direction is [-,+,-,+] and the spd command is in mm/s. 

`$upload:0,0,0#` 
Reports the encoder data, each digit controls the reporting of specific encoder information. 
The only important one for us is $upload:0,0,1# which toggles constant reporting of the wheel speed (in mm/s) in this format:
`$MSPD:M1,M2,M3,M4#`.
This should be sent once at startup to toggle reporting.