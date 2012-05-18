#!/bin/sh

rm /tmp/chasco/tmva_scratch/MC_ZZ_0/tmva/test/TMVAClassificationApplication.C
cp TMVAClassificationApplication_MC_ZZ_0.C /tmp/chasco/tmva_scratch/MC_ZZ_0/tmva/test/TMVAClassificationApplication.C
 cd /tmp/chasco/tmva_scratch/MC_ZZ_0/tmva/test
root -l TMVAClassificationApplication.C
cd -
