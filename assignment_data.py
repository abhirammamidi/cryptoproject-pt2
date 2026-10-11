"""Assignment 1 reference data.

The numeric instances below are the same A-H instances supplied by the group
member's test-data file, reorganised for the Part-1 solvers in this project.
This module deliberately keeps the secret exponents separate from INSTANCES:
solvers must recover x from (g, h, p), never read x_secret.

Public solver contract
----------------------
INSTANCES[label] contains only parameters a solver may legitimately consume.
TEST_SECRETS is optional verification data for local testing only.

Keys used by this project:
    p, g, h, order, factors
    q                 safe-prime q for F/G/H
    B_ic, B_ls, M_ls  algorithm-specific tuning parameters
"""

from types import MappingProxyType

# ---------------------------------------------------------------------------
# Canonical public DLP instances.
# ---------------------------------------------------------------------------
_RAW = {
    "A": {
        "p": 693167,
        "g": 164335,
        "h": 259584,
        "order": 693166,
        "factors": {2: 1, 127: 1, 2729: 1},
        "bits": 20,
        "tasks": ("bruteforce", "bsgs"),
        "note": "brute force; BSGS",
    },
    "B": {
        "p": 23786429,
        "g": 9362370,
        "h": 4638124,
        "order": 23786428,
        "factors": {2: 2, 5946607: 1},
        "bits": 25,
        "tasks": ("bruteforce", "bsgs"),
        "note": "brute-force timing; BSGS",
    },
    "C": {
        "p": 60550941570467,
        "g": 41285179178312,
        "h": 24567263929513,
        "order": 738426116713,
        "factors": {738426116713: 1},
        "bits": 46,
        "tasks": ("bsgs", "rho"),
        "note": "prime-order BSGS + Pollard rho",
    },
    "C2": {
        "p": 173824560813461,
        "g": 136909103735260,
        "h": 91621553091930,
        "order": 8691228040673,
        "factors": {2907871: 1, 2988863: 1},
        "bits": 48,
        "tasks": ("rho",),
        "note": "composite-order Pollard rho; gcd branch",
    },
    "D": {
        "p": 53655850852080155211649597313774387,
        "g": 42542276943417154811668320110417768,
        "h": 30813290145548005862557030942257434,
        "order": 53655850852080155211649597313774386,
        "factors": {
            2: 1, 678883: 1, 249383: 1, 261323: 1,
            565973: 1, 780889: 1, 1372027: 1,
        },
        "bits": 116,
        "tasks": ("pohlig_hellman",),
        "note": "116-bit prime; smooth squarefree group order",
    },
    "E": {
        "p": 287905742668293751,
        "g": 226534342114636353,
        "h": 31858198383945774,
        "order": 287905742668293750,
        "factors": {3: 8, 5: 5, 7: 4, 11: 3, 13: 3, 2: 1},
        "bits": 58,
        "tasks": ("pohlig_hellman",),
        "note": "prime-power order; digit lifting",
    },
    "F": {
        "p": 933730553927,
        "q": 466865276963,
        "g": 5,
        "h": 853489489347,
        "order": 933730553926,
        "factors": {2: 1, 466865276963: 1},
        "bits": 40,
        "tasks": ("index_calculus",),
        "note": "safe-prime index calculus",
        "B_ic": 180,
    },
    "G": {
        "p": 2732631930604127,
        "q": 1366315965302063,
        "g": 5,
        "h": 323700813070741,
        "order": 2732631930604126,
        "factors": {2: 1, 1366315965302063: 1},
        "bits": 52,
        "tasks": ("index_calculus", "linear_sieve"),
        "note": "safe-prime IC + linear sieve",
        "B_ic": 260,
        "B_ls": 220,
        "M_ls": 700,
    },
    "H": {
        "p": 13364832395624223587,
        "q": 6682416197812111793,
        "g": 2,
        "h": 386747052339436562,
        "order": 13364832395624223586,
        "factors": {2: 1, 6682416197812111793: 1},
        "bits": 64,
        "tasks": ("bonus",),
        "note": "64-bit safe-prime bonus instance",
    },
}

# Keep this name compatible with the run_all.py interface.
INSTANCES = _RAW

# Secret exponents are deliberately isolated from INSTANCES.
# They are for local verification/data validation only.
TEST_SECRETS = {
    "A": 149722,
    "B": 9336324,
    "C": 349412852845,
    "C2": 3623507350375,
    "D": 3048631699222626176292590840522770,
    "E": 38043505020760957,
    "F": 772419623157,
    "G": 565608321738391,
    "H": 4733727204259496922,
}

# ---------------------------------------------------------------------------
# Part-2 test messages/vectors retained from the supplied data set.
# ---------------------------------------------------------------------------
MESSAGES = [b'',
 b'abc',
 b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq',
 b'The quick brown fox jumps over the lazy dog',
 b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
 b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
 b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
 b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
 b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
 b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
 b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
 b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
 b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
 b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
 b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
 b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
 b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa']

SHA_VECTORS = {'sha256': {b'': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            b'abc': 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad',
            b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq': '248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1',
            b'The quick brown fox jumps over the lazy dog': 'd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592',
            b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': '9f4390f8d30c2dd92ec9f095b65e2b9ae9b0a925a5258e241c9f1e910f734318',
            b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': 'b35439a4ac6f0948b6d6f9e3c6af0f5f590ce20f1bde7090ef7970686ec6738a',
            b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': '6374f73208854473827f6f6a3f43b1f53eaa3b82c21c1a6d69a2110b2a79baad',
            b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': 'f54353008a2553262ecdc4a34749563ba0950e8b0fc8652780b0a614b99683c1',
            b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': '41edece42d63e8d9bf515a9ba6932e1c20cbc9f5a5d134645adb5db1b9737ea3'},
 'sha512': {b'': 'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e',
            b'abc': 'ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f',
            b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq': '204a8fc6dda82f0a0ced7beb8e08a41657c16ef468b228a8279be331a703c33596fd15c13b1b07f9aa1d3bea57789ca031ad85c7a71dd70354ec631238ca3445',
            b'The quick brown fox jumps over the lazy dog': '07e547d9586f6a73f73fbac0435ed76951218fb7d0c8d788a309d785436bbb642e93a252a954f23912547d1e8a3b5ed6e1bfd7097821233fa0538f3db854fee6',
            b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': 'b0220c772cbf6c1822e2cb38a437d0e1d58772417a4bbb21c961364f8b6143e05aa6316dca8d1d7b19e16448419076395f6086cb55101fbd6d5497b148e1745f',
            b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': '962b64aae357d2a4fee3ded8b539bdc9d325081822b0bfc55583133aab44f18bafe11d72a7ae16c79ce2ba620ae2242d5144809161945f1367f41b3972e26e04',
            b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': 'fa9121c7b32b9e01733d034cfc78cbf67f926c7ed83e82200ef86818196921760b4beff48404df811b953828274461673c68d04e297b0eb7b2b4d60fc6b566a2',
            b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': 'c01d080efd492776a1c43bd23dd99d0a2e626d481e16782e75d54c2503b5dc32bd05f0f1ba33e568b88fd2d970929b719ecbb152f58f130a407c8830604b70ca',
            b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': '67ba5535a46e3f86dbfbed8cbbaf0125c76ed549ff8b0b9e03e0c88cf90fa634fa7b12b47d77b694de488ace8d9a65967dc96df599727d3292a8d9d447709c97'},
 'sha3_256': {b'': 'a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a',
              b'abc': '3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532',
              b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq': '41c0dba2a9d6240849100376a8235e2c82e1b9998a999e21db32dd97496d3376',
              b'The quick brown fox jumps over the lazy dog': '69070dda01975c8c120c3aada1b282394e7f032fa9cf32f4cb2259a0897dfc04',
              b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': '78c2a04624b9328ae0e40cb8cdd29980f6ff55abf2dca68e3412d09eed4b9d03',
              b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': 'f6fe8de5c8f5014786f07e9f7b08130f920dd55e587d47021686b26cf2323deb',
              b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': '9d012f691de29b3ddbd82efd48f55233cc805a597e4bac48a560974679050897',
              b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': '25b135a86f4912961363e247a5d77f9dfaba85ae5d5e937e3aaec62054856e9e',
              b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': '8f3934e6f7a15698fe0f396b95d8c4440929a8fa6eae140171c068b4549fbf81'}}


def validate_instances():
    """Validate structural consistency without using any external library."""
    for name, inst in INSTANCES.items():
        p, g, h = inst["p"], inst["g"], inst["h"]
        n = inst["order"]
        if not (1 < g < p and 1 <= h < p):
            raise ValueError(f"{name}: invalid residue range")
        if pow(g, n, p) != 1:
            raise ValueError(f"{name}: g does not have order dividing order")
        if sum(1 for _ in inst["factors"]) == 0:
            raise ValueError(f"{name}: missing factorisation")
        reconstructed = 1
        for q, e in inst["factors"].items():
            reconstructed *= q ** e
        if reconstructed != n:
            raise ValueError(f"{name}: factors do not reconstruct order")
        if pow(g, TEST_SECRETS[name], p) != h:
            raise ValueError(f"{name}: supplied verification exponent is inconsistent")
    return True


if __name__ == "__main__":
    validate_instances()
    print(f"Validated {len(INSTANCES)} DLP instances: {', '.join(INSTANCES)}")
