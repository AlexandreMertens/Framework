#include <cp3_llbb/Framework/interface/MuonsProducer.h>

void MuonsProducer::produce(edm::Event& event, const edm::EventSetup& eventSetup) {

    edm::Handle<std::vector<pat::Muon>> muons;
    event.getByToken(m_leptons_token, muons);

    edm::Handle<double> rho_handle;
    event.getByToken(m_rho_token, rho_handle);

    edm::Handle<std::vector<reco::Vertex>> vertices_handle;
    event.getByToken(m_vertices_token, vertices_handle);

    const reco::Vertex& primary_vertex = (*vertices_handle)[0];

    double rho = *rho_handle;

    for (const auto& muon: *muons) {
        if (! pass_cut(muon))
            continue;

        fill_candidate(muon, muon.genParticle());

        reco::MuonPFIsolation pfIso = muon.pfIsolationR03();
        computeIsolations_R03(pfIso.sumChargedHadronPt, pfIso.sumNeutralHadronEt, pfIso.sumPhotonEt, pfIso.sumPUPt, muon.pt(), muon.eta(), rho);

        pfIso = muon.pfIsolationR04();
        computeIsolations_R04(pfIso.sumChargedHadronPt, pfIso.sumNeutralHadronEt, pfIso.sumPhotonEt, pfIso.sumPUPt, muon.pt(), muon.eta(), rho);

        isLoose.push_back(muon.isLooseMuon());
        isMedium.push_back(muon.isMediumMuon());
        isSoft.push_back(muon.isSoftMuon(primary_vertex));
        isTight.push_back(muon.isTightMuon(primary_vertex));
        isHighPt.push_back(muon.isHighPtMuon(primary_vertex));

        ScaleFactors::store_scale_factors({static_cast<float>(fabs(muon.eta())), static_cast<float>(muon.pt())});
    }
}
