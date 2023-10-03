import os

debug = True
server_host = "localhost"
server_port = 5555
server_hostname = "localhost"
buff_size = 4096
tls = True
__tls_cert_dir = os.path.join(os.path.dirname(__file__), "ssl")
tls_cert_priv = os.path.join(__tls_cert_dir, "rootCA.key")
tls_cert_pub = os.path.join(__tls_cert_dir, "rootCA.pem")
