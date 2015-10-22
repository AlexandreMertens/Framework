
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
jetToolbox( process, 'ak8', 'ak8JetSubs', 'out', PUMethod='CHS', miniAOD=True, addPruning=True, addSoftDrop=True, addSoftDropSubjets=True, addNsub=True, Cut='')
#jetToolbox( process, 'ak8', 'ak8JetSubs', 'out', addSoftDrop=True, addSoftDropSubjets=True, addNsub=True, addTrimming=True ) 

#process.options.allowUnscheduled = cms.untracked.bool(True) # Why?
#process.framework.producers.fat_jets.parameters.jets = cms.untracked.InputTag('selectedPatJetsAK8PFCHS')

from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
## Select charged hadron subtracted packed PF candidates
process.pfCHS = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string("fromPV"))

## PATify pruned fat jets
addJetCollection(
    process,
    labelName = 'AK8PFCHSSoftDrop',
    jetSource = cms.InputTag('ak8PFJetsCHSSoftDrop'),
    btagDiscriminators = ['None'],
    jetCorrections = ('AK8PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None'),
    getJetMCFlavour = False, # jet flavor disabled
    svSource = cms.InputTag('slimmedSecondaryVertices'), # changing the source of secondary vertices
    pfCandidates = cms.InputTag('packedPFCandidates') # adding packed PF candidate source
)

    
## PATify soft drop subjets
addJetCollection(
    process,
    labelName = 'AK8PFCHSSoftDropSubjets',
    jetSource = cms.InputTag('ak8PFJetsCHSSoftDrop','SubJets'),
    algo = 'ak',  # needed for subjet flavor clustering
    rParam = 0.8, # needed for subjet flavor clustering
    btagDiscriminators = ['pfCombinedSecondaryVertexV2BJetTags', 'pfCombinedInclusiveSecondaryVertexV2BJetTags'],
    jetCorrections = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None'),
    explicitJTA = True,  # needed for subjet b tagging
    svClustering = True, # needed for subjet b tagging
    genJetCollection = cms.InputTag('slimmedGenJets'), 
    fatJets=cms.InputTag('ak8PFJetsCHS'),             # needed for subjet flavor clustering
    groomedFatJets=cms.InputTag('ak8PFJetsCHSSoftDrop'), # needed for subjet flavor clustering
    svSource = cms.InputTag('slimmedSecondaryVertices'), # changing the source of secondary vertices
    pfCandidates = cms.InputTag('packedPFCandidates') # adding packed PF candidate source
)


# change the genParticle collection to prunedGenParticles
process.patJetPartonMatchAK8PFCHSSoftDrop.matched = cms.InputTag("prunedGenParticles")
process.patJetPartonMatchAK8PFCHSSoftDropSubjets.matched = cms.InputTag("prunedGenParticles")
process.patJetPartons.particles = cms.InputTag("prunedGenParticles")
process.patJetPartonsLegacy.src = cms.InputTag("prunedGenParticles")

# cone info for SoftDrop (why?)
process.patJetGenJetMatchAK8PFCHSSoftDrop.matched = cms.InputTag("ak8GenJetsNoNu")
process.patJetGenJetMatchAK8PFCHSSoftDrop.maxDeltaR = cms.double(0.8)

# change the offlinePrimaryVertices to slimmedOfflinePriamtryVertices
process.pfImpactParameterTagInfos.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")
process.pfImpactParameterTagInfosAK8.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")
process.pfImpactParameterTagInfosAK8PFCHSSoftDropSubjets.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")
process.pfImpactParameterTagInfosCA15.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")

process.pileupJetIdCalculator.vertexes = cms.InputTag("offlineSlimmedPrimaryVertices")
process.pileupJetIdEvaluator.vertexes = cms.InputTag("offlineSlimmedPrimaryVertices")

process.softMuonTagInfos.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")
process.softPFMuonsTagInfosAK8.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")
process.softPFMuonsTagInfosCA15.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")

process.softPFElectronsTagInfos.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")
process.softPFElectronsTagInfosAK8.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")
process.softPFElectronsTagInfosCA15.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")

process.impactParameterTagInfos.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")
process.bVertexFilter.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")

process.ak4CaloL1OffsetCorrector.vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices")
process.ak4JPTL1OffsetCorrector.vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices")
process.ak4PFCHSL1OffsetCorrector.vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices")
process.ak4PFL1OffsetCorrector.vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices")

process.patJetCorrFactorsAK8PFCHSSoftDrop.primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices")
process.patJetCorrFactorsAK8PFCHSSoftDropSubjets.primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices")

process.bToCharmDecayVertexMerged.primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices")
process.bToCharmDecayVertexMerged.vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices")

'''
## creates slimmedJet 
process.slimmedJetsAK8PFCHSSoftDropSubjets = cms.EDProducer("PATJetSlimmer",
    src = cms.InputTag("selectedPatJetsAK8PFCHSSoftDropSubjets"),
    packedPFCandidates = cms.InputTag("packedPFCandidates"),
    dropJetVars = cms.string("1"),
    dropDaughters = cms.string("0"),
    rekeyDaughters = cms.string("1"),
    dropTrackRefs = cms.string("1"),
    dropSpecific = cms.string("1"),
    dropTagInfos = cms.string("1"),
    modifyJets = cms.bool(True),
    modifierConfig = cms.PSet( modifications = cms.VPSet() )
)
'''

## Establish references between PATified fat jets and subjets using the BoostedJetMerger
process.slimmedJetsAK8PFCHSSoftDropPacked = cms.EDProducer("BoostedJetMerger",
    jetSrc=cms.InputTag("selectedPatJetsAK8PFCHSSoftDrop"),
    subjetSrc=cms.InputTag("selectedPatJetsAK8PFCHSSoftDropSubjets")
)

process.packedPatJetsAK8 = cms.EDProducer("JetSubstructurePacker",
    jetSrc = cms.InputTag("selectedPatJetsAK8PFCHSSoftDrop"),
    distMax = cms.double(0.8),
    algoTags = cms.VInputTag(
        # NOTE: For an optimal storage of the AK8 jet daughters, the first subjet collection listed here should be
        #       derived from AK8 jets, i.e., subjets should contain either all or a subset of AK8 constituents.
        #       The CMSTopTag subjets are derived from CA8 jets later matched to AK8 jets and could in principle
        #       contain extra constituents not clustered inside AK8 jets.
        cms.InputTag("slimmedJetsAK8PFCHSSoftDropPacked"),
        #cms.InputTag("slimmedJetsCMSTopTagCHSPacked")
     ),
     algoLabels = cms.vstring(
         'SoftDrop',
         #'CMSTopTag'
         ),
     #fixDaughters = cms.bool(True),
     fixDaughters = cms.bool(False),
     packedPFCandidates = cms.InputTag("packedPFCandidates")
)

# switch off daughter re-keying since it's done in the JetSubstructurePacker (and can't be done afterwards)
#process.slimmedJetsAK8.rekeyDaughters = "0"
'''
slimmedJetsAK8 = cms.EDProducer("PATJetSlimmer",
   src = cms.InputTag("packedPatJetsAK8"),
   packedPFCandidates = cms.InputTag("packedPFCandidates"),
   dropJetVars = cms.string("1"),
   dropDaughters = cms.string("0"),
   rekeyDaughters = cms.string("1"),
   dropTrackRefs = cms.string("1"),
   dropSpecific = cms.string("0"),
   dropTagInfos = cms.string("0"),
   modifyJets = cms.bool(True),
   modifierConfig = cms.PSet( modifications = cms.VPSet() )
)
'''
process.framework.producers.fat_jets.parameters.jets = cms.untracked.InputTag('packedPatJetsAK8')
process.framework.producers.fat_jets.parameters.SoftDropSubjets = cms.untracked.string('selectedPatJetsAK8PFCHSoftDropSubjets')
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
