"""
Optional JOSE (application/jose) transport encryption for STARMF 2.0.

IMPORTANT — read before enabling STARMF_USE_ENCRYPTION=true
--------------------------------------------------------------------
The Postman collection only shows that the "Member Login (with Encryption
Headers)" call sends:

    Content-type: application/jose
    X-API-Org-ID: member/<code>:<api-key>
    body: <compact JWS/JWE string, header alg=RS256>

It does NOT document BSE's exact JOSE profile — e.g. whether the payload is
a signed JWS, an encrypted JWE, or a nested JWS-inside-JWE ("sign then
encrypt"), which content-encryption algorithm is used (A256GCM, A128CBC-HS256,
...), or which key-wrapping algorithm (RSA-OAEP-256, RSA1_5, ...). That detail
normally comes from BSE's separate API/onboarding documentation, not the
Postman export.

This module gives you a working, swappable implementation using the
`jwcrypto` library and the most common StAR-MF-style profile reported by
integrators (RS256 signature, RSA-OAEP-256 + A256GCM encryption). Treat the
constants below as configuration you MUST confirm against your own BSE
onboarding docs before using this in production — wrong assumptions will
simply cause BSE to reject the request with a generic error.

If you don't have the encryption spec yet, leave STARMF_USE_ENCRYPTION=false
and use the plain-JSON endpoints (Member Login, and every other endpoint in
the collection all support that mode).
"""
from __future__ import annotations

from pathlib import Path

from jwcrypto import jwe, jwk, jws
from jwcrypto.common import json_encode, json_decode

# Confirm these against BSE's documentation before production use.
SIGNING_ALG = "RS256"
KEY_WRAP_ALG = "RSA-OAEP-256"
CONTENT_ENC_ALG = "A256GCM"


def _load_key(path_or_pem: str) -> jwk.JWK:
    text = path_or_pem
    if Path(path_or_pem).is_file():
        text = Path(path_or_pem).read_text()
    return jwk.JWK.from_pem(text.encode())


def sign_and_encrypt(payload: dict, *, sign_key_path: str, encrypt_key_path: str) -> str:
    """Sign the JSON payload with our private key, then encrypt the resulting
    JWS with the counterparty's (BSE's) public key. Returns a compact JWE
    string suitable for the request body when Content-type: application/jose.
    """
    signing_key = _load_key(sign_key_path)
    encrypting_key = _load_key(encrypt_key_path)

    signer = jws.JWS(json_encode(payload).encode())
    signer.add_signature(
        signing_key, alg=SIGNING_ALG, protected=json_encode({"alg": SIGNING_ALG})
    )
    signed = signer.serialize(compact=True)

    encrypter = jwe.JWE(
        signed.encode(),
        protected=json_encode({"alg": KEY_WRAP_ALG, "enc": CONTENT_ENC_ALG}),
    )
    encrypter.add_recipient(encrypting_key)
    return encrypter.serialize(compact=True)


def decrypt_and_verify(token: str, *, decrypt_key_path: str, verify_key_path: str) -> dict:
    """Reverse of sign_and_encrypt: decrypt the JWE with our private key, then
    verify the inner JWS with the counterparty's public key. Returns the
    decoded JSON payload.
    """
    decrypting_key = _load_key(decrypt_key_path)
    verifying_key = _load_key(verify_key_path)

    decrypter = jwe.JWE()
    decrypter.deserialize(token, key=decrypting_key)
    signed_payload = decrypter.payload.decode()

    verifier = jws.JWS()
    verifier.deserialize(signed_payload, key=verifying_key)
    verifier.verify(verifying_key)
    return json_decode(verifier.payload)
