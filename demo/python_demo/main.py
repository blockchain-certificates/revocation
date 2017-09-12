import ipfsapi
import json

#replace this part with ethereum connection :)
cert_id = "example_cert"
cert_test_rules_ipfs = "QmRpf56gT995wnmBwQsbiCAKRFZhHVpdcBkkAdQWjPUGze"
cert_test_proofs_ipfs = "QmTDLmKYLRxEw6Hjb8swSi1xDZvQs6R9jPb5isyZKPuXBX"



api = ipfsapi.connect('127.0.0.1', 5001)

def getJSONfromIPFS(ipfscat):
	res = api.cat(ipfscat)
	resjson = res.decode('utf8').replace("'", '"')

	return json.loads(resjson)

rulesFile = getJSONfromIPFS(cert_test_rules_ipfs)
proofsFile = getJSONfromIPFS(cert_test_proofs_ipfs)

def mockGetPublicKeyFromSignature(proof):
	if "issuer_revoke" == proof:
		return "issuer_key"

	if "receiver_revoke" == proof:
		return "receiver_key"

def getPublicKeyFromSignature(proof):
	return mockGetPublicKeyFromSignature(proof)

def verifyRevocationStatus(rulesFile, proofsFile):
	revocationStatus = True
	for proof in proofsFile["proofs"]:
		if getPublicKeyFromSignature(proof) not in rulesFile["revocation_rules"]:
			revocationStatus = False

	return revocationStatus
		

	


print(verifyRevocationStatus(rulesFile,proofsFile))
