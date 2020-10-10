# DS18B20 Temperature Sensor

## A `Python` script written for `RaspberryPi`

This *script* reads values from a DS18B20 Temperature Sensor connected to a raspberry pi via a 1-wire Data Line and writes said values to a file.

The `run` function lets you:
 * choose the delay between each reading
 * pick the file to be written to
 * choose whether to read and write 
   * indefinitely or
   * a definite number of times with this number set with said `run` function.
