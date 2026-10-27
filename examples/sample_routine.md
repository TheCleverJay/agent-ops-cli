# Goal
Scan inbox for ORDER mails and fulfill quietly.

## Trigger
Email to YOUR_FULFILLMENT_INBOX@example.com, plus weekday afternoon cron.

## Steps
1. List unprocessed order mail.
2. Verify payment read-only on a public explorer.
3. Ship zip + SHA256; record ledger.
When nothing is new, stay silent.
