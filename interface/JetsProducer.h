#ifndef JETS_PRODUCER
#define JETS_PRODUCER

#include <cp3_llbb/Framework/interface/CandidatesProducer.h>
#include <cp3_llbb/Framework/interface/BTaggingScaleFactors.h>

#include <DataFormats/PatCandidates/interface/Jet.h>


class JetsProducer: public CandidatesProducer<pat::Jet>, public BTaggingScaleFactors {
    public:
        JetsProducer(const std::string& name, const ROOT::TreeGroup& tree, const edm::ParameterSet& config):
            CandidatesProducer(name, tree, config), BTaggingScaleFactors(const_cast<ROOT::TreeGroup&>(tree))
        {
            BTaggingScaleFactors::create_branches(config);

            if (config.exists("btags")) {
                const std::vector<std::string>& btags = config.getUntrackedParameter<std::vector<std::string>>("btags");

                // Create branches 
                for (const std::string& btag: btags) {
                    m_btag_discriminators.emplace(btag, &CandidatesProducer<pat::Jet>::tree[btag].write<std::vector<float>>());
                }
            }
        }

        virtual ~JetsProducer() {}

        virtual void doConsumes(const edm::ParameterSet& config, edm::ConsumesCollector&& collector) override {
            m_jets_token = collector.consumes<std::vector<pat::Jet>>(config.getUntrackedParameter<edm::InputTag>("jets", edm::InputTag("slimmedJets")));
        }

        virtual void produce(edm::Event& event, const edm::EventSetup& eventSetup) override;

        float getBTagDiscriminant(size_t index, const std::string& name) const {
            return m_btag_discriminators.at(name)->at(index);
        }

    private:

        // Tokens
        edm::EDGetTokenT<std::vector<pat::Jet>> m_jets_token;

        std::map<std::string, std::vector<float>*> m_btag_discriminators;
    public:
        // Tree members
        std::vector<float>& area = tree["area"].write<std::vector<float>>();
        std::vector<int8_t>& partonFlavor = tree["partonFlavor"].write<std::vector<int8_t>>();
        std::vector<int8_t>& hadronFlavor = tree["hadronFlavor"].write<std::vector<int8_t>>();
        std::vector<float>& jecFactor = tree["jecFactor"].write<std::vector<float>>();
        std::vector<float>& puJetID = tree["puJetID"].write<std::vector<float>>();
        std::vector<float>& vtxMass = tree["vtxMass"].write<std::vector<float>>();

        BRANCH(passLooseID, std::vector<bool>);
        BRANCH(passTightID, std::vector<bool>);
        BRANCH(passTightLeptonVetoID, std::vector<bool>);
};

#endif
