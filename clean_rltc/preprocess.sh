#!/bin/sh
sed -i -re 's/”/"/g' *.txt
sed -i -re 's/“/"/g' *.txt
sed -i -re "s/’/'/g" *.txt
sed -i -re 's/»/"/g' *.txt
sed -i -re 's/«/"/g' *.txt
sed -i -re 's/<</"/g' *.txt
sed -i -re 's/>>/"/g' *.txt
sed -i -re 's/•//g' *.txt
sed -i -re "s/\`/'/g" *.txt
sed -i -re 's/<U+FEFF>//g' *.txt
sed -i -re 's/  / /g' *.txt

