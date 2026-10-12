# Core Unit Test Policy

Rule for this repository:

- No new use case in `src/dashboard/domain` or `src/dashboard/application`
  should be merged without at least 2-4 unit tests.
- Unit tests must cover expected behavior plus at least one relevant edge case.
- If a use case depends on adapters/IO, keep the core logic pure in
  application/domain and test that logic as `unit`.

This rule keeps core changes reviewable and prevents test debt from
accumulating during incremental refactors.
