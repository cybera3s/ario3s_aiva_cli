# aiva cli tool

<p>A tool to create SOCKS5 proxy on localhost</p>


## Configuration
<p>Default config file path is /home/USERNAME/.aiva.toml

<b>Config file Format</b>
```
[default]
username = "<DEFAULT USERNAME>"
local_port = <DEFAULT BIND PORT>
server_label = "<DEFAULT LABEL>"

[server_<label>]
ip = <server-ip>
port = <server-port>

[server_<label>]
...

```
</p>

## Usage

Connects to server using ssh
```
aiva connect  
```

Disconnects from server
```
aiva disconnect  
```

Get connection status
```
aiva status [-d] 
```

List available servers
```
aiva list_servers
```

Change default server
```
aiva change-server
```