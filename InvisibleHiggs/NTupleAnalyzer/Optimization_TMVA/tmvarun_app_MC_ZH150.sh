#!/bin/sh

rm /tmp/chasco/tmva_scratch/MC_ZH150/tmva/test/TMVAClassificationApplication.C
cp TMVAClassificationApplication_MC_ZH150.C /tmp/chasco/tmva_scratch/MC_ZH150/tmva/test/TMVAClassificationApplication.C
 cd /tmp/chasco/tmva_scratch/MC_ZH150/tmva/test
root -l TMVAClassificationApplication.C
cd -
