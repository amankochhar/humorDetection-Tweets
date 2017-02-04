#!/bin/bash

DATA_DIR=./word2vec-master/data
BIN_DIR=./word2vec-master/bin
SRC_DIR=./word2vec-master/src

TEXT_DATA='/home/AmanKochhar/nltk_data/corpora/wordnet'
TEXT_DATA=$DATA_DIR/text8
#ZIPPED_TEXT_DATA="${TEXT_DATA}.zip"
VECTOR_DATA=$DATA_DIR/answers.bin

pushd ${SRC_DIR} && make; popd

if [ ! -e $VECTOR_DATA ]; then
  time $BIN_DIR/word2vec -train $TEXT_DATA -output $VECTOR_DATA -cbow 0 -size 200 -window 100 -negative 0 -hs 1 -sample 1e-3 -threads 12 -binary 1
  
fi

$BIN_DIR/distance $DATA_DIR/$VECTOR_DATA $1
