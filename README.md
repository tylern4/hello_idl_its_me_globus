# Hello World Tests for IDL with Globus

1. First edit [config.yaml](config.yaml) for your machine.  Configure endpoint on target machine. 
```bash
globus-compute-endpoint configure --endpoint-config config.yaml hello
globus-compute-endpoint start hello
```
Copy endpoint id into [hello.env](hello.env).

2. Copy function files [hello.py](hello.py) and [hello.pro](hello.pro) to path on target machine.
2. Edit functions in [register_hello.py](register_hello.py) by replacing the path to function files in the variable `command`.
3. Register functions:
```shell
python register_hello.py
```
4. Run functions:
```shell
python hello_test.py --type idl
```
Wait until all IDL functions have completed.  Then run python functions.
```shell
python hello_test.py --type python
```
5. Plot results:
```shell
python plot_hello.py
```
