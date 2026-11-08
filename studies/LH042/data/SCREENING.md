# LH042 screening and redaction log

What was removed from retained bodies, and why. Every read log (`readlog.csv` in each data directory) keeps `sha256_as_fetched`, the hash of the bytes received; the bodies on disk differ from those bytes only as listed here.

## IPv4 addresses (all reads)

scripts/fetch.py replaces every IPv4 address with `x.x.x.x` before a body is written (the keeper's caution of 8 November 2026: no address of any host is retained). Per-body counts are in each readlog's `ipv4_redacted` column; `sha256_saved` is the hash after that step and before the later steps below.

## Host screening

scripts/screen_hosts.py was run over every body on 8 November 2026 (about 19:27 UTC). No IPv4 address remained; no IPv6 address appeared in any page's visible text; the hostnames in visible text were page furniture, documentation links, example names (`api.example.com`, `my-llm.duckdns.org` given as a vanity-name example, `node01.example.com` in Shadowserver's sample row, `evil-c2.example.com` on DECLAWED's page), lists of hosting providers' reverse-DNS suffixes in the Ollama paper's appendix, and a proxy SDK's endpoint quoted in Synthient's analysis. None is a list of exposed hosts, so nothing was removed for this reason. No page whose content is a list of exposed hosts was fetched.

## A key quoted in a page

round1-2026-11-08/034.body (Synthient): one API-key string shown in a quoted request of the proxy SDK Synthient analysed was replaced with `[redacted-by-Lighthouse]`, about 19:28 UTC. SHA-256 after that step: 2cd0a21d3cd68b08725f1169d9be1a7fc557acd98c9756c1f2c2f4433ad628f1 (before the email step below).

## Email addresses (the keeper, 8 November 2026)

`python3 -I scripts/redact_emails.py studies/LH042` was run at about 19:31 UTC, after all five collection rounds and the dashboard read had been saved, and before the record was committed. fetch.py now does the same before saving. One body, data/dash-2026-11-08T1909Z/001.body, had already been committed with one address in it (commit 20ca9a9); the redacted body replaces it at the next commit, and the earlier blob stays in git history. The tool's log, one line per file changed:

```
studies/LH042/data/dash-2026-11-08T1909Z/001.body	1 replaced	sha256 before aeb2cb384ccfb40ec0ef6dcbeb5567fa9d7be10a2929e93714262a719ec19f5f	after 0e5b2b2985c9008d36e1bf46c488f94a0d2dfc59dd8165f628ed8f89abe4e598
studies/LH042/data/round1-2026-11-08/002.body	8 replaced	sha256 before e5193c0ba2b781b4356f551397786445acf66c96c5260e9f35eadac6f84a5ecb	after 9d2179337536e0607d4ccc78181c2eaad47a5e08a78f393883ace5be1f5977b0
studies/LH042/data/round1-2026-11-08/004.body	2 replaced	sha256 before 1d9f72f31ea70e7f8c649a3d9fdf1f9d5fe15b5bf2804b22c1d2e694244ca017	after 2d7f8fe039ed721e0d2030b8d94d9c0981dfb88812af9c8ede78071cc7ed2d2b
studies/LH042/data/round1-2026-11-08/009.body	2 replaced	sha256 before c3495c673bb13f9f2d71b8a6e3ccda06d6064770740ea9e426211bb9dd14f7f7	after 2c4a44639c799ab9182ab69939238507ddf00d79eadb4235b03a2b8566d552cb
studies/LH042/data/round1-2026-11-08/010.body	2 replaced	sha256 before ed96336f49b34baa378dac78ff35a5ad35c3b14d66836cabd73e716f906ced33	after 89b02b7e2e3738ea23c1c676cf57bd799483993eb5ab055f0368b05a72c06f75
studies/LH042/data/round1-2026-11-08/015.body	2 replaced	sha256 before da797e43d580ca470fe0e40ce370d546258d54b37bab6a47107a420550210244	after 7ebb415513b728ac52027131b82e179ac49a88a3e482e90f1927c6bbed4de1bb
studies/LH042/data/round1-2026-11-08/016.body	2 replaced	sha256 before d716773e258b1390da5290a94974c5fa0daafe8c91c7fca2fad3035c425d02e7	after e31937a5fcbee3782e34fa2c617ab1df0f410da3bc90de72f2ec897f9dc1317a
studies/LH042/data/round1-2026-11-08/017.body	2 replaced	sha256 before fc34fa5df7621f161feacfee032d76f28b0150136db92eb5bfda8235f7bd3ecf	after d8622fc59677ece600b2ad68b75429370e73ce46c6115c2f3f008f5f3da4fc00
studies/LH042/data/round1-2026-11-08/018.body	1 replaced	sha256 before 10b14bf8f9562135357ad3e16e035d05868454adf5f3d7b77472ba78cc8b0c8c	after 919a5321d48e6cfcb9a0e25bc3da18f6c0ba4534e9fd0806e14aac8011934040
studies/LH042/data/round1-2026-11-08/019.body	1 replaced	sha256 before 3bd456df3b923abe4d371ad1eda0c454523df106d43d1a3be26e5f1ed98ca6c2	after 80ab06f059d0922cf3476c08529488bad3cf875a3be0a1c288ee14d71bfe5576
studies/LH042/data/round1-2026-11-08/020.body	1 replaced	sha256 before c38ab1475cfc093f7c7416ae8b20265382948c0233d7399e35065ce1b8471767	after 7dc1266d32abd3bfc2623e4d02dbaec4b9586f63b135c0b040858cfc7cf261ee
studies/LH042/data/round1-2026-11-08/022.body	2 replaced	sha256 before 028073fe0c4daf2c6ca414a5fcf2fe3d41356109b11d9480706edca9ddc28657	after 7c7bb33f5a49cedfbfe6a0fca6cbf318dc8eecaf08ae316bbe552474f220b107
studies/LH042/data/round1-2026-11-08/023.body	2 replaced	sha256 before a97a1786c89960afcfb69fc9c8a2dd2894e182098bdb8a264370f455012f3c89	after e6a56c1297a269c3988a0c407b8926aacaece6425e0946e4ba8a3d031a4300eb
studies/LH042/data/round1-2026-11-08/024.body	2 replaced	sha256 before 10dd39d7e2715748687b9e35c9f5c1652ff0c356d1122251d20c45e9fbfc9dcd	after 0e7a298dcff470a586e696b9b4f2f4c80880dd44bfe786a31bf4c3856efabac3
studies/LH042/data/round1-2026-11-08/026.body	1 replaced	sha256 before 28c73117a962274164042e2950a6ac02bf7550a4c09cd80dbb5a4bc09644f598	after 193a09609fbd9a9b17f0cf70d4049966650068a046695212120a2fce6c6baaf2
studies/LH042/data/round1-2026-11-08/028.body	3 replaced	sha256 before 6a3e5b9407e20cb6189d25cec7f1f68444749196b741559d5df4d46ac4d5bedd	after de61bc6286f95aa95b36c8e6c5f23cd86967bc9bf4a8ed32e0097a1a5525a7ec
studies/LH042/data/round1-2026-11-08/034.body	2 replaced	sha256 before 2cd0a21d3cd68b08725f1169d9be1a7fc557acd98c9756c1f2c2f4433ad628f1	after 94fbdac02c105f7fe942f74078e0f35f8beda75ddea9fa57a383ffea123ea451
studies/LH042/data/round2-2026-11-08/001.body	12 replaced	sha256 before 371ff3d63f87790cc62cd311b55a11230bfca7b564a2cdcb8910d4183c1e023b	after 6cf9990163fe27c48413eff043d66dfd222d9902dbba9a22b201c84f40a3f19a
studies/LH042/data/round2-2026-11-08/002.body	8 replaced	sha256 before 8ea0be7c56ce33e7e3a6568fe2152cd1debb1dd92af969d30be7d2fb12299827	after 2e6c9897c6e129a5656d8ac9491dad9162b7ca96e4b0a0c55c0a0c30abc31d0f
studies/LH042/data/round2-2026-11-08/003.body	1 replaced	sha256 before a2427b55800190d552a512555601232211fbc4ef088cd8b4c8c11b83e1119644	after 873706953effee0e8bd0a98b8cab249dcf4e81050e6ffca2bfa70e0cbbf45b47
studies/LH042/data/round2-2026-11-08/005.body	1 replaced	sha256 before a58477d9ec8d051773cdfb4ee226124a1547b5670175f0e78a76dea854c5d214	after fd3f0eed703965d697de11d1c9b331cd93831b354bae7b16fe9e262ce546d43e
studies/LH042/data/round2-2026-11-08/007.body	5 replaced	sha256 before a0c0c05100e67029af85428d9567b1d731358e879ad29d33867fc0762fc9d44f	after 807cfd8a16cbad94f57ab4cb65c534511d7145409eeda686e0684ef41e159819
studies/LH042/data/round2-2026-11-08/008.body	3 replaced	sha256 before ca26eb69e8b7e45937e3495a0147c972bd76a11e1b9017483aa7e45658b71306	after 6f3d9ff1ca25c0b37cef21545e108b159d704ab8a18bbc3d487f3bb81aa5e951
studies/LH042/data/round3-2026-11-08/001.body	12 replaced	sha256 before e1c05953533f0901693115b9b876e7ec54bf73515c58ab1a37aafdb91ffc6557	after e6084c3f7ea95f6dbc562c3724fc918c3de995dd7887345cdfe6fe261891b601
studies/LH042/data/round3-2026-11-08/002.body	12 replaced	sha256 before 0798cdfd382ccae50f065f302053cd1778e4aa2abef33ae2e05bd26e89fba972	after d7a229cf28b3920da102841720dee7434ec3ffd0f11b40a8c989c804073f64b0
studies/LH042/data/round3-2026-11-08/003.body	8 replaced	sha256 before 2729a2fa189842caf4a98b0dcd349875ff8cffa3723fe86919acddeccc4ed08d	after d0c06c7a119e000e7da9d87af5dafc8440c0afceee3e824646249489697c01e5
studies/LH042/data/round3-2026-11-08/004.body	8 replaced	sha256 before 465f3b4c991be8e43750b728f760a3dcf92d3a8bbe17af56f21287c68dbde1a5	after 80fe9dec97b1def7ded0551afe564fe1b63951c8fb573d74d2fcff6f7c977b1e
studies/LH042/data/round3-2026-11-08/005.body	16 replaced	sha256 before ba1b920d98cfc83391d4cc167675fc7280b2ab640e849a4409ec603378a9e670	after f5615648eaa81e72b37cd89b6625fbc37f4e0d2bae062187251baec12273efec
studies/LH042/data/round3-2026-11-08/006.body	12 replaced	sha256 before cc90dbf8edcfac544097ccb2ef9add0fe7eb4d636ceae05d142e3a281b251fb4	after 476aaea6a1db11568a1008651f4cb8e8ad715fee9dd772181ae20b6135b9e2bc
studies/LH042/data/round3-2026-11-08/007.body	12 replaced	sha256 before dd697949c648e0a2e40b838d8d83a7b3e0b2a404533405db81c74865b69487b4	after 10d57e0c9a5d525473ee6a7ad9adf8b69f50e159eb73ba1b9d63382f3963a915
studies/LH042/data/round4-2026-11-08/001.body	8 replaced	sha256 before bb75236986affc70d1a11d0997daf1c7ce36948d3adfe9f6d76b6a2fcd8eff6e	after 49fb171988294915b95e5319251aa4a53ee5c33bf16b21d35a41709333021da2
studies/LH042/data/round4-2026-11-08/002.body	8 replaced	sha256 before 52da5659a9c7df0a4347434aca91351a05e03eebc817b41014df9d51e9537468	after b4f3e07fa377970929d04333fd9a5a8592c73492c8148860d24d7dfb59b2093a
studies/LH042/data/round5-2026-11-08/001.body	1 replaced	sha256 before 8b16655fa1bc56a469d150c2cb785cf7318537b88ba95ddcaa869037572e1a42	after bbc6cab04c311d51a50e437c98f44d6aaa5bf4f939609a18c23fd44152a75275
```
