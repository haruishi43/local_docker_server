# Local Docker Server

Local docker server that you can use to create users and ssh into them

__NOTE__: heavily refactoring right now -- no more shell scripts!

## Installation

```
pip install -r requirements.txt
pip intall -e .
```

## How to run

- Tinker with the `configs`
- `python tools/build_images.py`
- `python tools/run_containers.py`

## Development

### TODO:

- [ ] clean up `tests` and make it better
- [ ] make `tools` better using arguments
