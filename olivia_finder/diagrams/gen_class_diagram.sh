#!/bin/bash

rm -r *.svg

pyreverse -o svg -d . -p olivia_finder ../olivia_finder --colorized --max-color-depth=6


# Obtener el tipo de letra que el usuario proporciona como primer argumento
font="$1"

# Comprobar que se ha proporcionado un tipo de letra
if [ -z "$font" ]; then
  echo "Debe proporcionar un tipo de letra como primer argumento."
  exit 1
fi

# # Comprobar que el tipo de letra está instalado en el sistema
# if ! fc-list | grep -i "$font" >/dev/null; then
#   echo "La fuente $font no está instalada en el sistema."
#   exit 1
# fi

# Cambiar el tipo de letra en todas las etiquetas de texto en el archivo SVG
sed -i "s/font-family=\"[^\"]*\"/font-family=\"$font\"/g" classes_olivia_finder.svg

# Cambiar el color de los bordes de las figuras a negro
sed -i 's/stroke="[^"]*"/stroke="black"/g' classes_olivia_finder.svg
