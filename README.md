# NATS and Config Replace Minions

A simple idea to get network configuration minions running with NATS.

If you'd like to run this project:

- Docker installed
- Access to EOS images or modify topology file with whatever image you have available
- Python3 installed
- Containerlab installed

## Build the runner image

```shell
docker build -t nats-config:latest .
```

## Build the watcher image

```shell
docker build -t nats-watcher:latest . -f Watchfile
```

## Run the Clab topology

```shell
sudo clab deploy -t topo.yml
```

## Make changes and watch the updates happen

Either install additional tooling to run AVD or manually modify one of the configuration files.

```shell
pip3 install "pyavd[ansible-collection]==5.1.0"
ansible-galaxy collection install arista.avd:=5.1.0
ansible-playbook playbooks/build.yml
```
