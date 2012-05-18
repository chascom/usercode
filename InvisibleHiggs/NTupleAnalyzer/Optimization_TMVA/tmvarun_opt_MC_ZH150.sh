#!/bin/sh

rm /tmp/chasco/tmva_scratch/MC_ZH150/tmva/test/TMVAClassification.C
cp TMVAClassification_MC_ZH150.C /tmp/chasco/tmva_scratch/MC_ZH150/tmva/test/TMVAClassification.C
 cd /tmp/chasco/tmva_scratch/MC_ZH150/tmva/test
root -l TMVAClassification.C
cd -
