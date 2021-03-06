
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
from cp3_llbb.Framework import Framework

process = Framework.create(True, eras.Run2_50ns, '74X_dataRun2_v2', redoJEC=True)

process.source.fileNames = cms.untracked.vstring(
        'file:///afs/cern.ch/user/s/sbrochet/public/CP3/DoubleMuon-Run2015B-17Jul2015-v1-MiniAOD_reduced.root'
        )

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
