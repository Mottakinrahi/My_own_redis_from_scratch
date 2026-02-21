# Redis Clone – In-Memory Database with TTL, AOF & Redis-Compatible Responses (Built from Scratch in Python)

A Redis-inspired in-memory key-value database built entirely from scratch in Python.

This project replicates core internal behaviors of real Redis, including:

- In-memory storage engine
- TTL with hybrid expiration (lazy + active)
- Append-Only File (AOF) persistence
- Background cleanup tasks
- Redis-compatible response formatting (RESP-style protocol)

The goal is to deeply understand how systems like Redis operate internally — from networking to memory management and durable logging.

---

## 🚀 Core Features

### 🔹 In-Memory Storage Engine
- O(1) key-value operations
- Type-aware storage
- Expiration metadata embedded with keys
- Real-time memory usage tracking

### 🔹 TTL (Time-To-Live) Support
- `EXPIRE`
- `EXPIREAT`
- `TTL`
- `PTTL`
- `PERSIST`
- `SET key value EX seconds`

### 🔹 Hybrid Expiration Strategy
Implements Redis-style expiration:

1. **Lazy Expiration**
   - Keys validated on access
   - Expired keys removed immediately

2. **Active Expiration**
   - Background cleanup every 100ms
   - Probabilistic key sampling (Redis-style)
   - Prevents memory leaks from inactive expired keys

### 🔹 Redis-Compatible Responses (RESP-like)

The server formats responses similar to real Redis using RESP-style output:

Examples:

```text
+PONG
```

```text
$5
hello
```

```text
:1
```

```text
-ERR unknown command
```

This makes the server behavior closely resemble real 
:contentReference[oaicite:0]{index=0}
response patterns.

---

### 🔹 AOF (Append-Only File) Persistence
- Logs every write operation
- Human-readable format with timestamps
- Crash-safe recovery
- Configurable fsync policies:
  - `always`
  - `everysec`
  - `no`
- Background AOF rewriting (`BGREWRITEAOF`)
- Atomic file replacement
- Full dataset reconstruction on restart

---

# 🏗 Architecture Overview

Single-threaded event loop architecture:

1. Network I/O (`select`)
2. Client request handling
3. Background TTL cleanup
4. Persistence sync tasks

Modular components:

- RedisServer (network + event loop)
- CommandHandler (command routing)
- DataStore (storage + TTL logic)
- PersistenceManager (AOF coordination)
- AOFWriter (disk logging)
- RecoveryManager (startup replay)

This design ensures:
- Non-blocking behavior
- Clean separation of concerns
- High throughput under single-threaded model

---

# 📦 Clone & Run the Project

## 🔹 Clone the Repository

```bash
git clone https://github.com/Mottakinrahi/My_own_redis_from_scratch.git
cd My_own_redis_from_scratch
```

## 🔹 Run the Server

Ensure Python 3.9+ is installed.

```bash
python3 main.py
```

Server starts on:

```text
localhost:6379
```

---

# 🔌 Connect Using Telnet

Open another terminal:

```bash
telnet localhost 6379
```

Now interact using Redis-style commands.

---

# 🧪 Example Commands

## Basic Operations

```text
PING
SET name Mottakin
GET name
DEL name
EXISTS name
```

## TTL Commands

```text
SET session abc EX 10
TTL session
PERSIST session
```

## AOF Rewrite

```text
BGREWRITEAOF
```

---

# 📊 Performance Characteristics

| Operation | Time Complexity |
|-----------|-----------------|
| SET       | O(1) |
| GET       | O(1) |
| DEL       | O(1) |
| TTL       | O(1) |
| Background Cleanup | O(k), k ≤ 20 |

---

# 🎯 Project Objective

This project demonstrates:

- Internal mechanics of Redis-style expiration
- Durable logging via AOF
- Event-driven server design
- RESP-style protocol formatting
- Recovery and file compaction strategies
- Systems-level backend engineering concepts

---

# 📜 License

MIT License
