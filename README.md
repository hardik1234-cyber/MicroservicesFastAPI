# Event-Driven-System

## Important UV Commands (Microservices)

### Initialize the Monorepo

```bash
uv init
```

Creates the root `pyproject.toml`.

---

### Create a New Microservice

```bash
uv init --app services/user-service
```

Creates a separate Python application structure and package configuration for the microservice.

---

### Install Dependencies for a Specific Service

```bash
uv add "fastapi[standard]" --package user-service
```

Adds the dependency to the `user-service` package.

Example:

```bash
uv add sqlalchemy --package user-service
uv add pydantic --package user-service
```

---

### Run a Specific Microservice

```bash
uv run fastapi dev main.py --port 8001
```

Example:

```bash
uv run fastapi dev services/user-service/main.py --port 8001
```

---

# gRPC Setup

## Install gRPC Dependencies

```bash
uv add grpcio grpcio-tools --package product-service
```

Installs:

- `grpcio` → Runtime library
- `grpcio-tools` → Proto compiler

---

## Create Proto Directory

```text
protos/
└── product.proto
```

All service contracts should be stored in the shared `protos` folder.

---

## Generate Python Files from Proto Contract

```bash
uv run python -m grpc_tools.protoc \
-I protos \
--python_out=services/product-service \
--grpc_python_out=services/product-service \
protos/product.proto
```

Generated files:

```text
services/product-service/
├── product_pb2.py
└── product_pb2_grpc.py
```

---

## Understanding Generated Files

### product_pb2.py

Contains generated message classes.

Example:

```python
ProductRequest
ProductResponse
```

---

### product_pb2_grpc.py

Contains generated gRPC classes.

Example:

```python
ProductServiceServicer
ProductServiceStub
```

---

## Regenerate Proto Files After Contract Changes

Whenever `product.proto` is modified:

```bash
uv run python -m grpc_tools.protoc \
-I protos \
--python_out=services/product-service \
--grpc_python_out=services/product-service \
protos/product.proto
```

---

## Example Proto Contract

```proto
syntax = "proto3";

package product;

service ProductService {
    rpc GetProduct(ProductRequest) returns (ProductResponse);
}

message ProductRequest {
    int32 id = 1;
}

message ProductResponse {
    int32 id = 1;
    string name = 2;
    float price = 3;
}
```

---

## Run gRPC Server

```bash
uv run python grpc_server.py
```

Default gRPC port:

```text
50051
```

---

## Communication Flow

```text
Client (User Service)
        |
        | gRPC Request
        ▼
Product Service
        |
        | ProductResponse
        ▼
Client
```

---

## Common gRPC Ports

```text
Product Service : 50051
User Service    : 50052
Order Service   : 50053
```

---

## Useful Commands

### Verify Generated Files

```bash
dir services/product-service/*pb2*
```

### Reinstall gRPC Dependencies

```bash
uv add grpcio grpcio-tools --package product-service
```

### Remove Dependency

```bash
uv remove grpcio --package product-service
```