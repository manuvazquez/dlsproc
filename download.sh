#!/bin/bash

OUTPUT_DIR=data/agregados

FILES=( 
    # yearly
    PlataformasAgregadasSinMenores_2018.zip
    PlataformasAgregadasSinMenores_2019.zip
    PlataformasAgregadasSinMenores_2020.zip
    PlataformasAgregadasSinMenores_2021.zip
    # monthly
    PlataformasAgregadasSinMenores_202201.zip
    PlataformasAgregadasSinMenores_202202.zip
    PlataformasAgregadasSinMenores_202203.zip
    PlataformasAgregadasSinMenores_202204.zip
    PlataformasAgregadasSinMenores_202205.zip
    PlataformasAgregadasSinMenores_202206.zip
)

mkdir -p $OUTPUT_DIR
pushd $OUTPUT_DIR

for f in "${FILES[@]}"
do
    
    # if it already exists...
    if test -f "$f"; then
    
        echo skipping \""$f"\"...it already exists
    
    # if the directory does NOT exist...
    else
    
        FULL_URL=https://contrataciondelsectorpublico.gob.es/sindicacion/sindicacion_1044/$f
    
        echo =================== downloading \""$f"\"  ===================
        
#         echo wget $FULL_URL
        
        wget $FULL_URL
    
    fi
    
done
