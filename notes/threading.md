## Threading Explained
- threading → run multiple tasks at the same time


### *** Sequential vs Threading

| Type       | Behavior                          |
|------------|-----------------------------------|
| Sequential | One request runs, others wait     |
| Threading  | Multiple requests run together    |

---
| Sequential (Blocking) | Threading (Parallel)   |
|-----------------------|------------------------|
| Request 1 (running)   | Request 1 (running)    |
| Request 2 (waiting)   | Request 2 (running)    |
| Request 3 (waiting)   | Request 3 (running)    |

**# NOTE:**
- Sequential = queue (one after another)
- Threading = concurrent execution (overlapping work)
--------------
### *** Thread basics

**1. create thread
```python
t = threading.Thread(target=scan_payload, args=(vuln, payload))
```
- target → function to run
- args → parameters

**2. start thread
```python
t.start()
```
- starts execution immediately

**3. join threads
```python
for t in threads:
    t.join()
```
- wait for ALL threads to finish
------------------
### *** join() confusion
| Type        | Usage           |
|-------------|-----------------|
| `''.join()` | Merge strings   |
| `t.join()`  | Wait for thread |
---------------
### *** Thread Count Problem
```python
for payload in tests:
    t = threading.Thread(...)
    t.start()
```
**? Meaning:**
- each payload → new thread
> 1000 payloads → 1000 threads 𖠋

**𖤾 problems:**
- high CPU usage
- high RAM usage
- system may crash

**⇨ hence:**
- not scalable
- unsafe in real-world
------------------
### *** ThreadPoolExecutor (Better Solution)

*** syntax
```python
from concurrent.futures import ThreadPoolExecutor
```
*** usage
```python
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(scan_payload, payloads)
```
**? Meaning:**
- max_workers ⇢ number of active threads (only 10 threads run at the same time)
- executor.map → applies function to all items 

ⶆ BUT ↬ runs in parallel
---------------------
### *** ThreadPoolExecutor Concept

- fixed number of threads (max_workers)
- tasks stored in a queue

**Execution flow:**
- First batch → threads take initial tasks
- When a thread finishes → it takes next task from queue
- Threads are reused until all tasks finish

⇨ No new threads are created
⇨ Tasks are distributed dynamically
⇨ This is controlled parallelism (not sequential, not full parallel)