#!/bin/bash

# Chemin vers l'image sprite sheet
SPRITESHEET_PATH="Flowers_Red.png"

# Nom de base pour les images séparées
OUTPUT_BASE=""

# Dimensions d'un personnage individuel (256x256 dans cet exemple)
WIDTH=32
HEIGHT=32

# Nombre de personnages par ligne et colonne
COLUMNS=24
ROWS=1

# Index de départ pour les noms de fichiers
INDEX=1

# Boucle sur les lignes
for ((row=0; row<$ROWS; row++)); do
  # Boucle sur les colonnes
  for ((col=0; col<$COLUMNS; col++)); do
    # Calcul des coordonnées du personnage dans la sprite sheet
    X=$(($col*$WIDTH))
    Y=$(($row*$HEIGHT))

    # Nom du fichier de sortie
    OUTPUT_FILE="${OUTPUT_BASE}_$(printf "%02d" $INDEX).png"

    # Utilisation de ImageMagick pour extraire le personnage
    convert "$SPRITESHEET_PATH" -crop ${WIDTH}x${HEIGHT}+${X}+${Y} "$OUTPUT_FILE"

    # Incrémentation de l'index
    INDEX=$((INDEX+1))
  done
done

echo "Images séparées avec succès."
