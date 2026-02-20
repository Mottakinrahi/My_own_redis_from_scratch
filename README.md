# Redis from Scratch: AOF Persistence Implementation

A lightweight, high-performance Redis clone built in Python. This project implements the **Append-Only File (AOF)** persistence mechanism, providing high data durability by logging every write operation to a journal-like file.

## 🚀 Key Features
- **In-Memory Data Store:** Fast key-value storage with support for Strings and TTL (Time-to-Live).
- **AOF Logging:** Every write command (SET, DEL, EXPIRE) is recorded in a human-readable format.
- **Configurable Fsync Policies:**
  - `always`: Maximum durability (sync every command).
  - `everysec`: Balance of speed and safety (default).
  - `no`: Maximum performance (OS handles syncing).
- **AOF Rewriting (Compaction):** Supports `BGREWRITEAOF` to reduce file size by removing redundant commands.
- **Automatic Recovery:** Replays logs on startup to restore the exact state of the database.

## 🏗️ System Architecture
The system is built with a non-blocking, event-driven architecture using Python's `select` module.



### Component Roles:
- **RedisServer:** Handles the network layer and event loop.
- **PersistenceManager:** Coordinates AOF writing and background tasks.
- **AOFWriter:** Manages the physical file I/O and synchronization policies.
- **RecoveryManager:** Reconstructs the dataset from the AOF log during boot.

## 🛠️ Installation & Usage

### 1. Clone the Repository
```bash
git clone [https://github.com/Mottakinrahi/My_own_redis_from_scratch.git](https://github.com/Mottakinrahi/My_own_redis_from_scratch.git)
cd My_own_redis_from_scratch