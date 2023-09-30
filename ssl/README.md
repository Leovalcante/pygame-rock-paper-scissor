# README.md

Follow these steps before trying to run any code.

1. First, generate a Certificate Authority (CA).

`openssl genrsa -out rootCA.key 2048`

2. Second, self-sign it.

`openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 365 -out rootCA.pem`

3. Next, install that CA on the system(s) you want to use it on. You'll have to find out how/where to install it for your system.
4. After that, create a certificate for each device you want to use it for.

`openssl genrsa -out device.key 2048`

Then, generate a certificate signing request.

`openssl req -new -key device.key -out device.csr`

**Pay careful attention the "Common Name" field. It must be the same as the common name for the CA, even if it's an IP address.**

5. Then, sign the CSR using the root-CA.

`openssl x509 -req -in device.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out device.crt -days 364 -sha256`

6. Finally, install the key and the certificate in your device(s).

## References

- https://datacenteroverlords.com/2012/03/01/creating-your-own-ssl-certificate-authority/
- https://gist.github.com/marshalhayes/ca9508f97d673b6fb73ba64a67b76ce8
