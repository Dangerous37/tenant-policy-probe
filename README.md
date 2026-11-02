# Tenant Policy Probe

Exercise an authorization matrix against a local HTTP service using synthetic role tokens. Compare expected and observed status codes, especially for cross-tenant resource reads and mutations.

## Run locally

Use Python 3.12. The project uses the standard library. From the repository root:

```sh
python cli.py example.json
python -m unittest -v
```

The included example is synthetic. Pass a different UTF-8 JSON file to inspect your own input. The command prints JSON to stdout. Invalid input returns status 2 and an explanation on stderr. See [CONTRACT.md](CONTRACT.md) for input fields and interpretation.

## Operational limits

IPv4 loopback only. PUT probes can change the selected test service. Use disposable tokens and synthetic resources. The demo uses a fixed sample policy with tenants A and B. Redirect responses are reported directly.

## Resumen en español

Ejecuta peticiones reales contra un servicio local para detectar fugas entre inquilinos y permisos de escritura excesivos.
