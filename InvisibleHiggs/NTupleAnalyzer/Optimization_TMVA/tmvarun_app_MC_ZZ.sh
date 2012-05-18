#!/bin/sh

rm /tmp/chasco/tmva_scratch/MC_ZZ/tmva/test/TMVAClassificationApplication.C
cp TMVAClassificationApplication_MC_ZZ.C /tmp/chasco/tmva_scratch/MC_ZZ/tmva/test/TMVAClassificationApplication.C
 cd /tmp/chasco/tmva_scratch/MC_ZZ/tmva/test
root -l TMVAClassificationApplication.C
cd -
