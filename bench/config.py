from __future__ import annotations

import os
from dataclasses import dataclass, field


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


@dataclass
class Neo4jConfig:
    uri: str = _env("NEO4J_URI", "bolt://localhost:7687")
    user: str = _env("NEO4J_USER", "neo4j")
    password: str = _env("NEO4J_PASSWORD", "")
    database: str = _env("NEO4J_DATABASE", "neo4j")


@dataclass
class NeptuneConfig:
    endpoint: str = _env("NEPTUNE_ENDPOINT", "lineage-bench.cluster-c45ky00a8417.us-east-1.neptune.amazonaws.com") 
    port: int = int(_env("NEPTUNE_PORT", "8182"))
    region: str = _env("NEPTUNE_REGION", "us-east-1")
    access_mode: str = _env("NEPTUNE_ACCESS_MODE", "bolt")
    iam_auth: bool = _env("NEPTUNE_IAM_AUTH", "false").lower() == "true"

    @property
    def bolt_uri(self) -> str:
        return f"bolt+s://{self.endpoint}:{self.port}"

    @property
    def https_url(self) -> str:
        return f"https://{self.endpoint}:{self.port}"

    @property
    def enabled(self) -> bool:
        return bool(self.endpoint.strip())


@dataclass
class DataConfig:
    data_dir: str = _env("BENCH_DATA_DIR", "data")
    n_source_systems: int = int(_env("BENCH_N_SOURCES", "40"))
    n_datasets: int = int(_env("BENCH_N_DATASETS", "1200"))
    n_fields: int = int(_env("BENCH_N_FIELDS", "18000"))
    n_transformations: int = int(_env("BENCH_N_TRANSFORMS", "3500"))
    n_reports: int = int(_env("BENCH_N_REPORTS", "600"))
    n_controls: int = int(_env("BENCH_N_CONTROLS", "900"))
    seed: int = int(_env("BENCH_SEED", "42"))
    load_batch_size: int = int(_env("BENCH_BATCH", "1000"))


@dataclass
class RunConfig:
    iterations: int = int(_env("BENCH_ITER", "6"))
    warmup: int = int(_env("BENCH_WARMUP", "1"))
    timeout_s: int = int(_env("BENCH_TIMEOUT", "120"))
    results_dir: str = _env("BENCH_RESULTS_DIR", "results")


@dataclass
class Config:
    neo4j: Neo4jConfig = field(default_factory=Neo4jConfig)
    neptune: NeptuneConfig = field(default_factory=NeptuneConfig)
    data: DataConfig = field(default_factory=DataConfig)
    run: RunConfig = field(default_factory=RunConfig)


CONFIG = Config()
