#!/bin/sh

rm /tmp/chasco/tmva_scratch/MC_ZZ/tmva/test/TMVAClassification.C
cp TMVAClassification_MC_ZZ.C /tmp/chasco/tmva_scratch/MC_ZZ/tmva/test/TMVAClassification.C
 cd /tmp/chasco/tmva_scratch/MC_ZZ/tmva/test
root -l TMVAClassification.C
cd -
