#platform-observer/

```
├── observer/
│
│   ├── collectors/
│   │      cpu.py
│   │      memory.py
│   │      disk.py
│   │      network.py
│   │      processes.py
│   │      docker.py
│   │      kubernetes.py
│   │      aws.py
│   │
│   ├── models/
│   │      cpu.py
│   │      memory.py
│   │      disk.py
│   │      network.py
│   │      process.py
│   │      node.py
│   │
│   ├── services/
│   │      scanner.py
│   │      reporter.py
│   │
│   ├── utils/
│   │      logger.py
│   │      config.py
│   │      decorators.py
│   │      exceptions.py
│   │
│   ├── concurrency.py
│   │
│   └── main.py
│
├── tests/
│
├── pyproject.toml
│
└── README.md
