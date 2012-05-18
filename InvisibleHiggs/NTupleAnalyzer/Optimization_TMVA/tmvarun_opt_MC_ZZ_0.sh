#!/bin/sh

rm /tmp/chasco/tmva_scratch/MC_ZZ_0/tmva/test/TMVAClassification.C
cp TMVAClassification_MC_ZZ_0.C /tmp/chasco/tmva_scratch/MC_ZZ_0/tmva/test/TMVAClassification.C
 cd /tmp/chasco/tmva_scratch/MC_ZZ_0/tmva/test
root -l TMVAClassification.C
cd -
