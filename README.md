# Redis Clone – In-Memory Database with TTL & AOF (Built from Scratch in Python)

A Redis-inspired in-memory key-value database built from scratch in Python.

This project implements Redis-style TTL (Time-To-Live) expiration strategies and durable persistence using an Append-Only File (AOF) mechanism — all within a single-threaded, non-blocking event loop architecture.

The goal of this project is to deeply understand how real-world systems like Redis manage:

- In-memory storage
- Key expiration strategies
- Background task scheduling
- Event-driven network servers
- Durable persistence via command logging
- Crash recovery and AOF rewriting

---

## 🚀 Core Features

### 🔹 In-Memory Storage Engine
- O(1) key-value operations
- Type-aware storage
- Memory usage tracking
- Efficient metadata management

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
   - Keys checked on access
   - Expired keys deleted immediately

2. **Active Expiration (Background Cleanup)**
   - Runs periodically in event loop
   - Probabilistic sampling (max 20 keys per cycle)
   - Prevents memory leaks from unused expired keys

### 🔹 AOF (Append-Only File) Persistence
- Logs every write operation
- Human-readable log format
- Crash-safe recovery
- Configurable fsync policies:
  - `always`
  - `everysec`
  - `no`
- Background AOF rewriting (`BGREWRITEAOF`)
- Atomic file replacement
- Full dataset recovery on restart

### 🔹 Event-Driven Server Architecture
- Single-threaded `select()` based event loop
- Non-blocking I/O
- Background task integration
- Clean modular design:
  - RedisServer
  - CommandHandler
  - DataStore
  - PersistenceManager
  - AOFWriter
  - RecoveryManager

---

# 🏗 Architecture Overview

The system follows a single-threaded event loop model:

1. Network I/O (via `select`)
2. Client request processing
3. Background TTL cleanup (every 100ms)
4. Persistence sync tasks

This ensures:
- High throughput
- Non-blocking behavior
- Efficient background processing
- Clean separation of concerns

---

# 📦 Clone & Run the Project

## 🔹 Clone the Repository

```bash
git clone https://github.com/Mottakinrahi/My_own_redis_from_scratch.git
cd My_own_redis_from_scratch
```

## 🔹 Run the Server

Make sure Python 3.9+ is installed.

```bash
python3 main.py
```

The server will start on:

```text
localhost:6379
```

(Default Redis port)

---

# 🔌 Connect Using Telnet

Open another terminal:

```bash
telnet localhost 6379
```

Now you can interact with the server.

---

# 🧪 Supported Commands

## Basic Commands

```text
PING
ECHO hello
SET key value
GET key
DEL key
EXISTS key
KEYS *
FLUSHALL
TYPE key
INFO
```

## TTL Commands

```text
SET temp value EX 10
EXPIRE key 30
EXPIREAT key 1691234567
TTL key
PTTL key
PERSIST key
```

---

# 🔁 AOF Persistence

## How It Works

For every write operation:

1. Command executes in memory
2. Command is formatted
3. Appended to AOF buffer
4. Synced to disk based on policy

On restart:
- AOF file is replayed
- Dataset reconstructed
- TTL metadata restored

---

## 🔄 AOF Rewriting

To compact the AOF file:

```text
BGREWRITEAOF
```

Removes redundant commands and rewrites minimal dataset snapshot.

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

# 🧠 Technical Highlights

- Redis-style hybrid expiration model
- Probabilistic cleanup algorithm
- Memory accounting system
- Atomic file replacement for safe AOF rewriting
- Recovery mechanism with corruption handling
- Modular persistence layer
- Non-blocking event loop architecture

---

# 📌 Future Improvements

- RDB Snapshot support
- RESP protocol full compliance
- Replication support
- Thread pool / multi-core scaling
- Configurable eviction policies (LRU/LFU)
- Benchmark suite

---

# 🎯 Project Goal

This project is a deep systems-level implementation designed to understand:

- How Redis manages memory efficiently
- How TTL expiration works internally
- How durable logging ensures crash recovery
- How event-driven servers are structured
- How real-world in-memory databases are built

---

# 📜 License

MIT License

---

If you find this project useful, feel free to star the repository ⭐
