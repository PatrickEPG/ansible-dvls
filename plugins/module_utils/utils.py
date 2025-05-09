from ansible_collections.devolutions.dvls.plugins.module_utils.vaults import (
    get_vault_entry,
)


def get_sensible_value(server_base_url, token, vault_id, entries):
    fetched_secrets = {}

    if isinstance(entries, dict) and "data" in entries:
        entries = entries.get("data", [])

    if not isinstance(entries, list):
        return {"error": f"Expected list of entries, got {type(entries).__name__}"}

    for secret in entries:
        if not isinstance(secret, dict):
            continue

        entry_name = secret.get("name")
        if not entry_name or "id" not in secret:
            continue

        try:
            entry = get_vault_entry(server_base_url, token, vault_id, secret["id"])
            if isinstance(entry, dict) and "data" in entry:
                secret_data = entry["data"]
                if isinstance(secret_data, dict):
                    secret_data["secret_path"] = secret.get("path", "")
                fetched_secrets[entry_name] = secret_data
        except Exception as e:
            fetched_secrets[entry_name] = {"error": str(e)}

    return fetched_secrets
