import random
import time

# Pre-seeded professional vocabulary databases for realistic, diverse text generation.
CATEGORIES = ["Technology", "Medicine", "Finance", "General"]

TECH_SUBJECTS = [
    "Vector search engine", "FAISS similarity index", "FastAPI async handler",
    "SentenceTransformers embedding model", "SQLite persistent cache", "Neural network latency",
    "Kubernetes container scaling", "High-frequency algorithmic trading", "PostgreSQL indexing optimization",
    "Rust language compile times", "Distributed consensus protocol", "Large language model inference"
]
TECH_VERBS = [
    "accelerates the performance of", "implements an optimized version of", "resolves memory leak bottlenecks in",
    "proves sub-100ms p95 latency for", "utilizes hierarchical clustering on", "enables zero-downtime hot-swapping for",
    "leverages deep neural networks within", "analyzes parallel query execution of", "maximizes multi-threaded QPS inside"
]
TECH_OBJECTS = [
    "approximate nearest neighbor vector matching.", "high-dimensional semantic space representations.",
    "highly parallelized CPU computing pipelines.", "efficient binary BLOB cache persistence.",
    "distributed web application cluster state.", "dynamic benchmarking visual charts.",
    "complex relational database query planning.", "asynchronous event loop scheduler instances."
]

MED_SUBJECTS = [
    "CRISPR gene editing therapy", "Cardiovascular blood flow model", "Oncology clinical trials review",
    "Targeted mRNA vaccine delivery", "Neurotransmitter receptor binding", "AI-assisted diagnostic imaging",
    "Microbiome diversity mapping", "Chronic pain management protocol", "Synthetic antibody design synthesis"
]
MED_VERBS = [
    "suppresses the expression of", "stimulates cell regeneration inside", "targets specific mutated receptors in",
    "accelerates drug absorption times for", "restores optimal neurological signaling within", "analyzes long-term efficacy profiles of",
    "enhances genetic translation precision in", "maps metabolic pathway interactions for"
]
MED_OBJECTS = [
    "malignant tumor growth pathways.", "immunological cellular response dynamics.",
    "patient physiological cardiovascular health.", "synthetic molecular structure integrity.",
    "high-throughput clinical drug screenings.", "preventative health diagnostic frameworks.",
    "gut microbiome flora balancing agents.", "advanced neural plasticity models."
]

FIN_SUBJECTS = [
    "High-frequency algorithmic trading", "Federal reserve interest rate adjustments", "Inflation risk hedging models",
    "Decentralized liquidity pool yields", "Automated portfolio rebalancing strategies", "Global macroeconomic trends",
    "Corporate balance sheet analysis", "Microfinance loan repayment metrics", "Real estate market volatility indexes"
]
FIN_VERBS = [
    "offsets the systemic risk of", "maximizes yield optimization algorithms for", "predicts future market trends on",
    "hedges against hyper-inflation spikes in", "leverages automated derivatives trading within", "calculates return-on-equity variables for",
    "stabilizes liquidity and arbitrage across", "mitigates collateralized debt default rates in"
]
FIN_OBJECTS = [
    "highly volatile derivative commodity markets.", "decentralized protocol liquidity pools.",
    "sovereign debt bonds and currency pairings.", "diversified blue-chip equity asset models.",
    "algorithmic arbitrage risk equations.", "automated passive index fund allocations.",
    "microeconomic small-business credit indices.", "real estate capital gains forecasting matrices."
]

GEN_SUBJECTS = [
    "Sustainable organic gardening", "Modern urban green space planning", "Artisanal espresso coffee roasting",
    "Deep-sea thermal vent exploration", "Classic literature narrative arcs", "Renewable wind turbine efficiency",
    "Historical architectural preservation", "Amateur astronomy stargazing clubs", "Traditional sourdough bread fermentation"
]
GEN_VERBS = [
    "enhances the structural diversity of", "promotes communal engagement and appreciation for", "documents the historical evolution of",
    "harnesses optimal thermodynamic patterns for", "analyzes stylistic symbolism and metaphor within", "optimizes natural resource allocation for",
    "explores subterranean ecosystems present in", "celebrates the cultural heritage of"
]
GEN_OBJECTS = [
    "local urban community cooperative gardens.", "modern minimalist design and architectural concepts.",
    "specialty single-origin micro-lot coffee blends.", "remote hydro-thermal oceanic biology systems.",
    "Victorian-era literary works and journals.", "offshore wind generation power grids.",
    "ancient structural masonry construction methods.", "traditional fermentation culinary arts."
]

def generate_documents(count: int) -> list[dict]:
    """
    Generates N synthetic documents with realistic data structure.
    Optimized for raw speed to generate 100,000 documents in <10 seconds.
    """
    documents = []
    
    # Pre-select lists of choices for faster loop execution
    categories = [CATEGORIES[i % len(CATEGORIES)] for i in range(count)]
    
    # We pre-calculate random timestamps distributed over the last 30 days
    base_time = time.time()
    seconds_in_day = 86400
    timestamps = [base_time - random.randint(0, 30 * seconds_in_day) for _ in range(count)]
    
    for i in range(count):
        cat = categories[i]
        timestamp = timestamps[i]
        
        # Select matching vocabulary based on category
        if cat == "Technology":
            subject = TECH_SUBJECTS[i % len(TECH_SUBJECTS)]
            verb = TECH_VERBS[(i // len(TECH_SUBJECTS)) % len(TECH_VERBS)]
            obj = TECH_OBJECTS[(i // (len(TECH_SUBJECTS) * len(TECH_VERBS))) % len(TECH_OBJECTS)]
            
            # Make titles dynamic and unique
            title = f"Optimizing {subject} Performance (System {i + 1})" if i % 2 == 0 else f"Next-Gen {subject} Architecture (v{i + 1})"
            body = (
                f"This document discusses how the {subject.lower()} {verb} {obj} "
                f"We explore how implementing highly concurrent architectures can optimize performance parameters, "
                f"ensuring sub-millisecond scaling under high-throughput server workloads."
            )
        elif cat == "Medicine":
            subject = MED_SUBJECTS[i % len(MED_SUBJECTS)]
            verb = MED_VERBS[(i // len(MED_SUBJECTS)) % len(MED_VERBS)]
            obj = MED_OBJECTS[(i // (len(MED_SUBJECTS) * len(MED_VERBS))) % len(MED_OBJECTS)]
            
            title = f"Clinical Efficacy of {subject} (Trial {i + 1})" if i % 2 == 0 else f"Advancements in {subject} (Series {i + 1})"
            body = (
                f"Recent clinical findings show that {subject.lower()} {verb} {obj} "
                f"By profiling biological interactions, researchers have verified the therapeutic pathways "
                f"and achieved substantial positive health metrics with minimal patient side-effects."
            )
        elif cat == "Finance":
            subject = FIN_SUBJECTS[i % len(FIN_SUBJECTS)]
            verb = FIN_VERBS[(i // len(FIN_SUBJECTS)) % len(FIN_VERBS)]
            obj = FIN_OBJECTS[(i // (len(FIN_SUBJECTS) * len(FIN_VERBS))) % len(FIN_OBJECTS)]
            
            title = f"Macroeconomic Impact of {subject} (Index {i + 1})" if i % 2 == 0 else f"Analyzing {subject} Risk (Model {i + 1})"
            body = (
                f"Our financial research suggests that {subject.lower()} {verb} {obj} "
                f"By analyzing historic yield curves and arbitrage opportunities, trading systems can mitigate "
                f"asset volatility and optimize risk-adjusted capital returns in dynamic market environments."
            )
        else: # General
            subject = GEN_SUBJECTS[i % len(GEN_SUBJECTS)]
            verb = GEN_VERBS[(i // len(GEN_SUBJECTS)) % len(GEN_VERBS)]
            obj = GEN_OBJECTS[(i // (len(GEN_SUBJECTS) * len(GEN_VERBS))) % len(GEN_OBJECTS)]
            
            title = f"The Beauty of {subject} (Volume {i + 1})" if i % 2 == 0 else f"Modern Guide to {subject} (Issue {i + 1})"
            body = (
                f"This descriptive guide highlights how {subject.lower()} {verb} {obj} "
                f"By integrating classical knowledge with contemporary sustainable practices, "
                f"enthusiasts and professionals can revitalize traditional fields and foster community engagement."
            )
            
        word_count = len(body.split())
        
        doc = {
            "id": f"doc_{i + 1}",
            "title": title,
            "body": body,
            "category": cat,
            "timestamp": float(timestamp),
            "word_count": int(word_count)
        }
        documents.append(doc)
        
    return documents
