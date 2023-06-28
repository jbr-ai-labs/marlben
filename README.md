![logo](https://github.com/jbr-ai-labs/marlben/assets/22059171/cab386fb-3b49-4f02-b59a-49dd2de3cc9c)

[![PyPI version](https://badge.fury.io/py/marlben.svg)](https://badge.fury.io/py/marlben)
![marlben-tests](../../actions/workflows/python-package-conda.yml/badge.svg)

Marlben is a multi-agent reinforcement learning benchmark based on the [NeuralMMO](https://github.com/NeuralMMO/environment) game engine

## Installation
https://github.com/jbr-ai-labs/marlben/wiki/Quick-Start#installation

### Installation via Pip
`Python3.9` is required

```
pip install marlben
```

Installation with RLlib dependencies:
```
pip install marlben[rllib]
```

## Usage

https://github.com/jbr-ai-labs/marlben/wiki/Quick-Start#launching-an-environment

### Examples
Examples are located in `examples` folder
- `rllib_integration.py` demonstrates how to start learning process with default config for `Corridor` env
  - `rllib` installation is required
- `override_config.py` demonstrates how to customize configs by inheriting from default class
- `custom_map_generator.py` demonstrates how to customize map generation for any environment
- `custom_environment.py` demonstrates how to customize whole environment structure by overriding all building blocks of the benchmark

## Wiki
https://github.com/jbr-ai-labs/marlben/wiki
