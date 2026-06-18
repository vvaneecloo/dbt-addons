# dbt-addons

A small, focused dbt wrapper that handles the boring-but-critical stuff dbt doesn't do for you out of the box, starting with **Write-Audit-Publish (WAP) / blue-green deployment**.

Most dbt projects build, then hope. 

A model runs, lands directly in its production location, and only afterwards do you find out whether the data was actually correct.

`dbt-addons` flips that order for the cases where it matters: build into a staging location, audit it, and only publish to production if the audit passes.

```bash
pip install dbt-addons
```

```yaml
# packages.yml
packages:
  - git: "https://github.com/vvaneecloo/dbt-addons"
```

---

## Why WAP, and why it's harder than it sounds in dbt

Write-Audit-Publish is a simple idea: never let unvalidated data reach a table your stakeholders query.

1. **Write**: build the model into a temporary/staging relation instead of its final location.
2. **Audit**: run data tests (or custom checks) against that staging relation.
3. **Publish**: atomically swap the staging relation into place only if every audit passes. If anything fails, production is untouched.

dbt's native materializations don't give you this.

A standard `table` or `incremental` model writes directly to its target location: if a test fails, it fails *after* the bad data is already sitting where downstream consumers (and BI tools) can see it. 

`dbt test` runs as a separate, later step; there's no built-in mechanism to gate a publish on a test result for the *same run*.

Implementing WAP correctly inside dbt's execution model means handling:
- Atomic relation swaps that work consistently across materializations
- Failure and rollback paths that leave production untouched
- Keeping the workflow declarative — config in YAML/macros, not a bespoke orchestration script bolted on top

`dbt-addons` packages this pattern as a reusable set of macros, so you don't have to rebuild it per project.

---

## Quickstart

1. Install dbt-addons

```bash
pip install dbt-addons
```

2. Specify the addons you want to use directly in `dbt_project.yml`

```yaml
vars:
  dbt-addons:
    addons:
      - wap
      - any_other_addon
```

3. Run `dbta install` & create a PR to add associated macros to your dbt project

```bash
dbta install
```

You're done ! For more information about WAP, please check our [documentation](https://vvaneecloo.github.io/dbt-addons/).

---

## What's in here today

- ✅ **WAP** — write-audit-publish macros for safe, gated model builds
- 🚧 More addons may follow as real gaps come up: this repo isn't trying to be a do-everything toolkit, just a place for genuinely useful dbt patterns that don't exist elsewhere yet.

## Requirements

- `dbt-core >= 1.5.0`
- Python `>= 3.10`

## Documentation

Full docs: **https://vvaneecloo.github.io/dbt-addons/**

## Installing for local development

```bash
pip install -e ".[dev]"
```

This pulls in `dbt-duckdb`, used for local testing/integration tests without needing a warehouse connection.

## Contributing

Issues and PRs welcome. If you're hitting a dbt pain point you think belongs here, open an issue describing it: the bar is "does dbt-core or a well-known existing package already solve this," not "would this be nice to have."

## License

MIT
