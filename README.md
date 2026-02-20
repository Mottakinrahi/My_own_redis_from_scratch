# Redis from Scratch: AOF Persistence Implementation

A high-performance, asynchronous Redis-like key-value store built in Python. This project focuses on **Append-Only File (AOF)** persistence, providing strong durability by journaling every write operation to disk.

## 🏗️ System Architecture
The implementation follows a modular design, separating the network layer from the persistence engine to ensure non-blocking operations.



### Key Components:
- **RedisServer**: Manages TCP sockets and the `select()`-based event loop.
- **AOFWriter**: Handles logging and synchronization based on `always`, `everysec`, or `no` policies.
- **RecoveryManager**: Replays the AOF log on startup to reconstruct the dataset.
- **Background Rewriter**: Compacts large AOF files by removing redundant commands via `BGREWRITEAOF`.

## 🛠️ Installation & Setup

To get the server running on your local machine, follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/Mottakinrahi/My_own_redis_from_scratch.git](https://github.com/Mottakinrahi/My_own_redis_from_scratch.git)
cd My_own_redis_from_scratch