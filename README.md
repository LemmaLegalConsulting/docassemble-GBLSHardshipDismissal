# docassemble.GBLSHardshipDismissal

GBLS Hardship Dismissal

## Author

Rami Lorca



## Automated interview tests

The draft ALKiln workflow starts a fresh isolated docassemble server. The enabled configuration-boundary scenario verifies the missing-token ending; it does not cover successful reminder scheduling.

Successful completion requires a LegalServer Demo site, a test matter UUID, a current user UUID, and a valid API v2 bearer token. Add a `legalserver` mapping to the docassemble server configuration with the lowercase `<site>-demo` key containing `bearer` and a future `expiration` date. The interview asks for the matter UUID, site abbreviation, and site type `Demo`. Use synthetic client data in the authorized Demo matter. The matter must include the case number and email address used by metadata and reminders. Configure outbound email before testing reminder delivery.

These integration requirements are unresolved in this draft PR. No production credentials or test doubles are bundled with the isolated workflow.
