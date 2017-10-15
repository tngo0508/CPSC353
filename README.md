# CPSC353
## Project 1 Text In Image
Author: Thomas Ngo <br /> 
Instructor: Reza Nikoopour <br /> 
California University State, Fullerton

## Project Description

The design of this program is divided into two main parts that are encode and decode. Following these main functions, there are also 3 helper functions that do the change of the last significant bit(LSB), conversion between text and binary and vice versa. The scripting language is python3. 

## How to execute

Make sure you change user permission to execute the program
```
$ chmod u+x project.py
```
### To encode:
```
$ ./project.py -e <image> -r <file>.txt -o <output>.png
```
or
```
$ python3 project.py -e <image> -r <file>.txt -o <output>.png
```
### To decode:
```
$ ./project.py -d <image>.png
```
or
```
$ python3 project.py -d <image> 
```
### Summary of the usage
```
usage: project.py [-h] (-d | -e) [-r READ] [-o OUTPUT] image

Stegenography Project CPSC353

positional arguments:
  image                 location of the image

optional arguments:
  -h, --help            show this help message and exit
  -d, --decode          decode on an image mode RGB
  -e, --encode          encode on an image mode RGB
  -r READ, --read READ  human-readable file
  -o OUTPUT, --output OUTPUT
                        Name of output file
```
