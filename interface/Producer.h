#pragma once

#include <FWCore/PluginManager/interface/PluginFactory.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/Run.h>
#include <FWCore/Framework/interface/LuminosityBlock.h>
#include <FWCore/Framework/interface/EventSetup.h>
#include <FWCore/Framework/interface/ConsumesCollector.h>
#include <FWCore/Utilities/interface/InputTag.h>

#include <cp3_llbb/TreeWrapper/interface/TreeWrapper.h>
#include <cp3_llbb/Framework/interface/MetadataManager.h>

#include <cp3_llbb/Framework/interface/Types.h>

#include <vector>
#include <map>

namespace Framework {

    class Producer {
        public:
            Producer(const std::string& name, const ROOT::TreeGroup& tree_, const edm::ParameterSet& config):
                m_name(name),
                tree(tree_) {
                }

            virtual void produce(edm::Event&, const edm::EventSetup&) = 0;
            virtual void doConsumes(const edm::ParameterSet&, edm::ConsumesCollector&& collector) {}

            virtual void beginJob(MetadataManager&) {}
            virtual void endJob(MetadataManager&) {}

            virtual void beginRun(const edm::Run&, const edm::EventSetup&) {}
            virtual void endRun(const edm::Run&, const edm::EventSetup&) {}

            virtual void beginLuminosityBlock(const edm::LuminosityBlock&, const edm::EventSetup&) {}
            virtual void endLuminosityBlock(const edm::LuminosityBlock&, const edm::EventSetup&) {}

            // Disable copy of producer
            Producer(const Producer&) = delete;
            Producer& operator=(const Producer&) = delete;

        protected:
            std::string m_name;
            ROOT::TreeGroup tree;
    };

}

typedef edmplugin::PluginFactory<Framework::Producer* (const std::string&, const ROOT::TreeGroup&, const edm::ParameterSet&)> ExTreeMakerProducerFactory;
