
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
from cp3_llbb.Framework import Framework

from JMEAnalysis.JetToolbox.jetToolbox_cff import jetToolbox

from cp3_llbb.Framework import FatJetsProducer


process = Framework.create(False, eras.Run2_25ns, '74X_mcRun2_asymptotic_v2', cms.PSet(
    dilepton = cms.PSet(
        type = cms.string('dilepton_analyzer'),
        prefix = cms.string('dilepton_'),
        enable = cms.bool(True),
        categories_parameters = cms.PSet(
            mll_cut = cms.untracked.double(20)
            ),
        parameters = cms.PSet(
            standalone = cms.untracked.bool(True),
            muons_wp = cms.untracked.string('loose'),
            electrons_wp = cms.untracked.string('loose')
            )
        ),

    bTagsLoose = cms.PSet(
        type = cms.string('btags_analyzer'),
        prefix = cms.string('btags_CSVv2_loose'),
        enable = cms.bool(True),
        parameters = cms.PSet(
            discr_name = cms.untracked.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
            discr_cut = cms.untracked.double(0.605),
            eta_cut = cms.untracked.double(2.4),
            pt_cut = cms.untracked.double(30)
            )
        ),

    bTagsMedium = cms.PSet(
        type = cms.string('btags_analyzer'),
        prefix = cms.string('btags_CSVv2_medium'),
        enable = cms.bool(True),
        parameters = cms.PSet(
            discr_name = cms.untracked.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
            discr_cut = cms.untracked.double(0.89),
            eta_cut = cms.untracked.double(2.4),
            pt_cut = cms.untracked.double(30)
            )
        ),

    bTagsTight = cms.PSet(
        type = cms.string('btags_analyzer'),
        prefix = cms.string('btags_CSVv2_tight'),
        enable = cms.bool(True),
        parameters = cms.PSet(
            discr_name = cms.untracked.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
            discr_cut = cms.untracked.double(0.97),
            eta_cut = cms.untracked.double(2.4),
            pt_cut = cms.untracked.double(30)
            )
        ),

    test = cms.PSet(
        type = cms.string('test_analyzer'),
        prefix = cms.string('test_'),
        enable = cms.bool(True)
        )
    ), 
    
    redoJEC=True,

    )

#jetToolbox( process, 'ak8', 'jetSequence', 'out', PUMethod='CHS', miniAOD=True, addPruning=True, addSoftDrop=True, addSoftDropSubjets=True, addNsub=True, addTrimming=True, Cut='')
jetToolbox( process, 'ak8', 'ak8JetSubs', 'out', PUMethod='CHS', miniAOD=True, addPruning=True, addSoftDrop=True, addSoftDropSubjets=True, addNsub=True, addTrimming=True, Cut='')
#jetToolbox( process, 'ak8', 'ak8JetSubs', 'out', addSoftDrop=True, addSoftDropSubjets=True, addNsub=True, addTrimming=True ) 

#process.options.allowUnscheduled = cms.untracked.bool(True) # Why?
process.framework.producers.fat_jets.parameters.jets = cms.untracked.InputTag('selectedPatJetsAK8PFCHS')
process.framework.producers.fat_jets.parameters.SoftDropSubjets = cms.untracked.string('selectedPatJetsAK8PFCHSSoftDropSubjets')
process.framework.producers.fat_jets.parameters.Njettinesstau1 = cms.untracked.string('NjettinessAK8CHS:tau1')
process.framework.producers.fat_jets.parameters.Njettinesstau2 = cms.untracked.string('NjettinessAK8CHS:tau2')
process.framework.producers.fat_jets.parameters.Njettinesstau3 = cms.untracked.string('NjettinessAK8CHS:tau3')
process.framework.producers.fat_jets.parameters.cut = cms.untracked.string("pt > 20")

Framework.schedule(process, analyzers=['dilepton', 'bTagsLoose', 'bTagsMedium', 'bTagsTight', 'test'],
        producers=['event', 'gen_particles', 'hlt', 'vertices', 'electrons', 'muons', 'jets', 'fat_jets', 'met', 'nohf_met'])

process.source.fileNames = cms.untracked.vstring(
        '/store/mc/RunIISpring15MiniAODv2/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/00000/0014DC94-DC5C-E511-82FB-7845C4FC39F5.root'
        )

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))
