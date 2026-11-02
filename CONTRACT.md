# Probe contract
With demo=true start the bundled loopback service and run its role/tenant matrix. For another local fixture provide port, tokens (role alias to disposable bearer value), cases (method GET or PUT, path beginning with /, role alias, expected HTTP status). PUT uses a synthetic probe body. Output contains alias, path and response status. Never point it at production data.
