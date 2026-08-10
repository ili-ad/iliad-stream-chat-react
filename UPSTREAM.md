# Upstream inheritance

Official upstream is `GetStream/stream-chat-react`. The original Iliad source baseline is immutable tag `v13.1.0`, commit `c9802c782a3e47bd44873884260c13213b6ee380`. The Iliad downstream package is `@iliad/stream-chat-shim`.

The inheritance boundary is:

```text
GetStream UI source
        ↓
Iliad downstream Stream fork
        ↓
Jatte Stream-compatible adapter
        ↓
Jatte backend / transport
```

`@iliad/realtime` is not part of the Stream-derived UI fork. Jatte-specific authentication, room policy, WebSocket lifecycle, REST behavior, and backend semantics belong outside this repository.

The current source was reconciled as an exact snapshot from `ili-ad/jatte-headless` commit `08130d52bd18e865009c3df4be5e1e2828641224`, path `libs/stream-chat-shim`, after preserving the four historical Iliad package-only commits. The porting anchors and exact Git object identities are recorded in `ILIAD_PROVENANCE.json`.

## Remote topology

Clone this Iliad repository as `origin`, then configure official GetStream as `upstream`:

```bash
git remote add upstream https://github.com/GetStream/stream-chat-react.git
git fetch upstream --tags
```

## Exact-release upgrade procedure

1. Fetch official GetStream upstream and its tags.
2. Select and record an exact immutable Stream release tag and commit SHA.
3. Record the current Iliad fork SHA.
4. Create a dedicated upgrade branch.
5. Inspect that Stream release's notes and migrations.
6. Merge the exact selected upstream tag into the Iliad branch.
7. Resolve conflicts while preserving the Iliad compatibility contract.
8. Run downstream provenance/source checks and applicable tests.
9. Qualify the candidate in a disposable Jatte host checkout.
10. After review, create an immutable Iliad release.
11. Advance Jatte's submodule SHA only after qualification.

Never merge a floating upstream branch, `HEAD`, or “latest” into a production candidate.

## Test boundary

The package intentionally retains its Jatte workspace dependency on `chat-shim`. Full component and compatibility tests therefore run in the Jatte host qualification environment. Standalone CI enforces ancestry, provenance, exact reconciled-tree identity, the realtime dependency boundary, and repository-owned diff hygiene.
