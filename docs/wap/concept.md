# WAP Concept


## The problem

When dbt rebuilds a model, it replaces the table in-place. If the run fails halfway through, or if a data quality test catches an issue after the fact, bad data has already reached production.

## Write-Audit-Publish

WAP solves this by separating the build schema from the production schema:

```
┌─────────────────────────────────────────────────────┐
│                    staging schema                    │
│                                                      │
│   dbt run/build → models materialized here first    │
│   dbt tests    → run against staging                │
└──────────────────────┬──────────────────────────────┘
                       │ tests pass
                       ▼
┌─────────────────────────────────────────────────────┐
│                     prod schema                      │
│                                                      │
│   wap_deploy → atomic clone/copy from staging       │
│   consumers  → always see last known-good state     │
└─────────────────────────────────────────────────────┘
```

If any test fails, the publish step is skipped for that model. Production is never touched.


## Per-model granularity

WAP operates at the model level. If `stg_customers` passes all its tests but `fct_customers` fails, only `stg_customers` is promoted. The CLI reports which models were promoted and which were skipped:

```
1 of 2 START copying stg_customers .................................. [RUN]
1 of 2 OK stg_customers ............................................. [OK]
2 of 2 FAIL fct_customers ........................................... [FAIL]

[ PARTIAL ] PASS=1 FAIL=1 TOTAL=2
```
