#!/bin/sh

rm /tmp/chasco/tmva_scratch/MC_ZZ_1/tmva/test/TMVAClassificationApplication.C
cp TMVAClassificationApplication_MC_ZZ_1.C /tmp/chasco/tmva_scratch/MC_ZZ_1/tmva/test/TMVAClassificationApplication.C
 cd /tmp/chasco/tmva_scratch/MC_ZZ_1/tmva/test
root -l TMVAClassificationApplication.C
cd -
