# Frozen source and tool provenance

## Order 16

The complete order-16 source is regenerated at replay time by nauty 2.9.3:

```sh
/opt/homebrew/bin/geng -Cq -d3 -D3 16
```

On the development machine, the `geng` binary has SHA-256
`ad2f68adf733dbed7cad543841cfa329740596ee5cd136f17a0a17f6e744f5ad`.
The generated 3,874-row byte stream has SHA-256
`57104aba69a542707e11ebdd8d6105afc2ce56d78b45f2e1ff0db55c1fab9de2`;
the independent replay checks this stream digest from the graph rows embedded
in its certificate.  A different compatible `geng` build is acceptable only
if it emits exactly this stream.

## Orders 18--26

The literal graph6 inputs and logs are inherited from
`search/focused-theta-choice-through28-20260727`.  That package records the
regeneration command

```sh
snarkhunter n 4 S s C4 o g
```

using a frozen Snarkhunter 2.0b binary.  The input digests and row counts are:

| order | rows | SHA-256 |
|--:|--:|:--|
| 18 | 2 | `2660e7d5c8a351b4ed3d69f8df316e748e264a630c01328ea4bed43f96f78dfd` |
| 20 | 6 | `a65153d9dc38bebffca52b2c2ec05f194807b10ca097f50a551d5aab871244f1` |
| 22 | 31 | `2c3d91e55cb264450cf321e2299355f6cf0f5c2c60a83c99372a1d73ed5a4223` |
| 24 | 155 | `37ef068ab597c6cc882eb2121d9743464b0717bc4beefab4348ef4221b6a7456` |
| 26 | 1,297 | `1d2b95b9d412f5f6b8ccb788779bd685df23b3239bda8c7e9557266375519760` |

`SOURCES.sha256` also freezes the five retained generator logs.  Corpus
canonical completeness relies on the cited generator package.  The new
Python checker independently confirms that every literal row is simple,
cubic, biconnected, non-Tait, and cyclically 4-edge-connected.

## Retained order 34

The exact input is
`search/strong_snarks/source/strongsnarks_34_5_cyc4.g6`: seven rows,
Git blob `4bed72ba7e9cb4315dc5a9562198847cb0b86d45`, SHA-256
`2f087d5cbd1e97b1e10e7a5a064fe83d037872f838372e4d317c9d3f912fbf1f`.
The last repository commit touching it is
`c7d9ae420d9b75b03abe9babc8c60c6609452aae` (2026-07-28).

The package makes no upstream completeness claim for this seven-row file.
The independent checker verifies each row is simple, cubic, biconnected,
non-Tait, cyclically 4-edge-connected, and has girth at least five.

## Implementations and development environment

The primary program includes the previously frozen graph6/flow primitives in
`../d5-typed-cap-double-star-frontier-20260731/audit_d5_typed_cap_ports.cpp`,
whose SHA-256 is
`b4808ad07d19062c3e3da949b59ba6e0691a5bdb979e098b901f5e6c29f10db5`.

Development versions:

```text
Apple clang 21.0.0 (clang-2100.1.1.101), arm64-apple-darwin25.5.0
Python 3.14.5
nauty 2.9.3
```
