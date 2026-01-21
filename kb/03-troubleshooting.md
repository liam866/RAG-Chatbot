# Troubleshooting

Common issues and how to resolve them.

## Cannot Connect to Ollama

If the chatbot returns an error saying it cannot reach the Ollama server, here are the most common causes:

1.  **Incorrect IP Address**: Ensure the `OLLAMA_BASE_URL` in your `.env` file matches the IP address of the machine running Ollama. It must be reachable from the VM running the chatbot.
2.  **Firewall Issues**: A firewall on your host machine (e.g., macOS, Windows) or on the Ollama server might be blocking incoming connections. Ensure the port (default `11434`) is open.
3.  **Ollama Not Bound to LAN**: By default, some Ollama installations only listen on `127.0.0.1` (localhost). You must configure Ollama to listen on `0.0.0.0` or a specific network interface to accept connections from other machines. Check the Ollama documentation for how to set the `OLLAMA_HOST` environment variable.
4.  **Docker Networking**: The Docker container needs to be able to reach the Ollama IP address on your local network. Standard Docker networking should handle this, but ensure you don't have custom network configurations that would prevent outbound traffic from the container to your LAN.

## Port Conflict

If `docker compose up` fails with a port conflict error, it means another service on your VM is already using port `8000`. You can either stop the other service or change the port mapping in `docker-compose.yml`.

For example, to map the container's port `8000` to the host's port `8001`, change the `ports` section:

```yaml
ports:
  - "8001:8000"
```
