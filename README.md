# oidc-lab professos cli


## Prerequisite

* oidc-lab
* (optional) mitm proxy server installed in oidc-lab
* Python 3
```
pip install -r requirements.txt
```

## Usage

### Quickstart

Load and run a complete test. Generated could be found afterwards in results/mitreid-client/default/report/index.html
```
load rp mitreid-client
full_test
```

### Run tests

To run same tests as in full_test run:
```
load rp mitreid-client
create
learn
run --all
export
report
```

### Manual tests

Run manual tests, mitm proxy server script must be loaded in oidc-lab
```
load rp mitreid-server
create
learn
expose 40
run_pyscript pentest/mitreid-server-redirect.py
export
report
```