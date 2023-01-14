# aiva cli tool

<p>a tool to connect to server using ssh</p>
<p>it creates a SOCKS proxy on provided port default to 4321</p>


## Configuration
<p>Default config file path is /home/<username>/.aiva.toml

<b>Config file Format</b>

```
[server]
ip = <server-ip>
port = <connections-port>
username = '<username>'
```
</p>

## Usage

connects to server using ssh
```
aiva connect  
```

disconnects from server
```
aiva disconnect  
```
get connection status
```
aiva status  
```