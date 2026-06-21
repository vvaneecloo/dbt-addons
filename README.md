# dbt-addons

A small, focused dbt wrapper that handles the boring-but-critical stuff dbt doesn't do for you out of the box:

- ✅ **WAP**: write-audit-publish macros for safe, blue-green deployments
- 🚧 More addons may follow as real gaps come up


## Quickstart

📄 Check out our documentation website: [documentation](https://vvaneecloo.github.io/dbt-addons/).


## Requirements

- `dbt-core >= 1.5.0`
- Python `>= 3.10`

## Installing for local development

```bash
pip install -e ".[dev]"
```

This pulls in `dbt-duckdb`, used for local testing/integration tests without needing a warehouse connection.

## Contributing

Issues and PRs welcome. If you're hitting a dbt pain point you think belongs here, open an issue describing it: the bar is "does dbt-core or a well-known existing package already solve this," not "would this be nice to have."

## License

MIT
