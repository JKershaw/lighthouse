# Recovering the local protocol snapshots

**In short.** The reviewed work was committed locally before collection, but this workspace has no Git push credentials. Publication uses the connected GitHub API, with this small Git bundle preserving the original local commits and hashes. It contains this branch's unshared history, not another source collection or an independent timestamp certification.

The bundle is `local-protocol-history.bundle`, archived head `aefd3d02a015ed4653bd2c9948d7d9f57e1788f5`. It needs the already-public base commits `2a425068454922969c94d9e6c5f03100a707ff00` and `33a98224da71110e5d194869ae46eb301e06868d`. A full clone of the repository supplies them. The archive retains the original protocol `bb8a6e9`, checkpoint `68b7093`, source snapshot `e2f6cc1` and review snapshots cited by the record, including the former local identifier LH051. Current records use LH052; the brief explains that administrative alias.

From a full repository clone, verify and fetch the data objects without checking out or executing archived files:

```sh
git bundle verify notes/organisational-reliability/local-protocol-history.bundle
git fetch notes/organisational-reliability/local-protocol-history.bundle HEAD:refs/remotes/local-protocol-history/reliability
git show bb8a6e9:studies/LH051/brief.md
```

This preserves the exact local Git objects. Commit dates remain locally recorded dates, not external proof of when a collection happened. It adds no private operational data or full primary-source body. The archive excludes history already reachable from the completed scheduled pass.

Archive bytes: 121921. SHA-256: `10149073a2c6cf934051de386b51414a65222c8af4dafa033cd66e58be7d3a33`.
