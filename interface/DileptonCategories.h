#ifndef DILEPTONCATEGORIES_H
#define DILEPTONCATEGORIES_H

#include <cp3_llbb/Framework/interface/Category.h>

class MuMuCategory: public Category {
    public:
        virtual bool event_in_category_pre_analyzers(const ProducersManager& producers) const override;
        virtual bool event_in_category_post_analyzers(const ProducersManager& producers, const AnalyzersManager& analyzers) const override;
        virtual void register_cuts(CutManager& manager) override;
        virtual void evaluate_cuts_post_analyzers(CutManager& manager, const ProducersManager& producers, const AnalyzersManager& analyzers) const override;
};

class MuElCategory: public Category {
    public:
        virtual bool event_in_category_pre_analyzers(const ProducersManager& producers) const override;
        virtual bool event_in_category_post_analyzers(const ProducersManager& producers, const AnalyzersManager& analyzers) const override;
        virtual void register_cuts(CutManager& manager) override;
        virtual void evaluate_cuts_post_analyzers(CutManager& manager, const ProducersManager& producers, const AnalyzersManager& analyzers) const override;
};

class ElMuCategory: public Category {
    public:
        virtual bool event_in_category_pre_analyzers(const ProducersManager& producers) const override;
        virtual bool event_in_category_post_analyzers(const ProducersManager& producers, const AnalyzersManager& analyzers) const override;
        virtual void register_cuts(CutManager& manager) override;
        virtual void evaluate_cuts_post_analyzers(CutManager& manager, const ProducersManager& producers, const AnalyzersManager& analyzers) const override;
};

class ElElCategory: public Category {
    public:
        virtual bool event_in_category_pre_analyzers(const ProducersManager& producers) const override;
        virtual bool event_in_category_post_analyzers(const ProducersManager& producers, const AnalyzersManager& analyzers) const override;
        virtual void register_cuts(CutManager& manager) override;
        virtual void evaluate_cuts_post_analyzers(CutManager& manager, const ProducersManager& producers, const AnalyzersManager& analyzers) const override;
};

#endif