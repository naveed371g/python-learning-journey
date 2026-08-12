# Full Mail Server (docker-mailserver)

A production-capable mail server (SMTP + IMAP, real accounts, DKIM/SPF/DMARC,
spam + virus filtering) using [docker-mailserver](https://docker-mailserver.github.io/docker-mailserver/latest/).

## Files

- `compose.yaml` — the service definition and port mappings.
- `mailserver.env` — feature flags and tuning (TLS, spam, security, relay, etc.).
- `setup.sh` — wrapper around the built-in `setup` CLI for managing accounts.
- `docker-data/` — persisted mail, state, logs, and config (created on first run, git-ignored).

## 1. Configure your hostname

A real mail server needs a fully-qualified domain name (FQDN).

Edit `compose.yaml` and set `hostname:` to your mail host, e.g. `mail.example.com`.
The base domain of your email addresses (`example.com`) is derived from the accounts you create.

## 2. Choose a TLS strategy

Edit `SSL_TYPE` in `mailserver.env`:

- **Testing on your laptop:** `SSL_TYPE=self-signed` (or leave empty for no TLS).
- **Production:** `SSL_TYPE=letsencrypt` and mount your certs. See the
  [TLS docs](https://docker-mailserver.github.io/docker-mailserver/latest/config/security/ssl/).

## 3. Start the server

```bash
docker compose up -d
docker compose logs -f        # watch startup
docker compose ps             # health status
```

## 4. Create accounts

Accounts are created after the container is running:

```bash
chmod +x setup.sh

# add a mailbox (you'll be prompted for a password if omitted)
./setup.sh email add you@example.com 'strong-password'

# list accounts
./setup.sh email list

# add an alias
./setup.sh alias add postmaster@example.com you@example.com
```

## 5. Generate DKIM keys

```bash
./setup.sh config dkim
```

This writes DKIM keys under `docker-data/dms/config/opendkim/`. Publish the
generated TXT record in your DNS.

## 6. DNS records needed for real delivery

For mail to actually flow in/out over the internet, add these to your domain's DNS:

| Type  | Name                          | Value                                            |
|-------|-------------------------------|--------------------------------------------------|
| A     | `mail.example.com`            | your server's public IP                          |
| MX    | `example.com`                 | `mail.example.com` (priority 10)                 |
| TXT   | `example.com` (SPF)           | `v=spf1 mx ~all`                                  |
| TXT   | `mail._domainkey.example.com` | (DKIM value from step 5)                          |
| TXT   | `_dmarc.example.com`          | `v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com` |
| PTR   | (reverse DNS at your host/ISP)| `mail.example.com`                               |

Port **25 outbound** must be open — many ISPs/clouds block it by default.

## Client settings

| Protocol   | Host               | Port | Security       |
|------------|--------------------|------|----------------|
| SMTP (send)| `mail.example.com` | 587  | STARTTLS       |
| SMTP (send)| `mail.example.com` | 465  | implicit TLS   |
| IMAP (recv)| `mail.example.com` | 993  | implicit TLS   |

Log in with the full email address and its password.

## Common commands

```bash
docker compose up -d          # start
docker compose down           # stop
docker compose logs -f        # follow logs
./setup.sh help               # all account/config management commands
```

## Testing without real DNS

To try it locally without owning a domain:

- Set `SSL_TYPE=self-signed` (or empty) in `mailserver.env`.
- Create an account and connect a mail client (e.g. Thunderbird) to `localhost`
  on ports 587/993, accepting the self-signed cert.
- Outbound internet delivery won't work without proper DNS/PTR, but local
  send/receive between your own accounts will.
