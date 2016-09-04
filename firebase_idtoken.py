from google.appengine.api import memcache
from google.appengine.api import urlfetch

import jwt
import json
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm

from Crypto.Util.asn1 import DerSequence
from Crypto.PublicKey import RSA
from binascii import a2b_base64

from rfc822 import mktime_tz, parsedate_tz
import time

__all__ = ["verify_token"]

""" Try to register algorithm - ignore if it is already registered """
try:
    jwt.register_algorithm("RS256", RSAAlgorithm(RSAAlgorithm.SHA256))
except ValueError:
    pass

    
""" get certificate for key id, caches the certs using memcache """
def get_certificate(key_id):
    certs = memcache.get(key="www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com")

    if certs is None:
        result = urlfetch.fetch("https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com", validate_certificate=True)

        expire = mktime_tz(parsedate_tz(result.headers["expires"]))
        certs = json.loads(result.content)

        memcache.add("www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com", certs, time=expire)

    cert = certs.get(key_id)

    return cert

""" return a public key from a X509 certificate """
""" http://stackoverflow.com/questions/12911373/how-do-i-use-a-x509-certificate-with-pycrypto """
def pubkey_from_cert(cert):
    # Convert from PEM to DER
    lines = cert.replace(" ","").split()
    der = a2b_base64("".join(lines[1:-1]))

    # Extract subjectPublicKeyInfo field from X.509 certificate (see RFC3280)
    cert = DerSequence()
    cert.decode(der)
    tbsCertificate = DerSequence()
    tbsCertificate.decode(cert[0])
    subjectPublicKeyInfo = tbsCertificate[6]

    # Initialize RSA key
    rsa_key = RSA.importKey(subjectPublicKeyInfo)

    return rsa_key
    
""" Parse and verify id token for specified audience """
def verify_token(token, audience):
    header = jwt.get_unverified_header(token)

    cert = get_certificate(header["kid"])
    if cert is None:
        raise ValueError("Cannot verify token - key not found")

    public_key = pubkey_from_cert(cert)

    return jwt.decode(token, public_key, audience=audience, algorithms=["RS256"])