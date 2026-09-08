 """# FastAPI File Upload — Complete Notes

## 1. What I learned today

Today I learned the basics of uploading files to a FastAPI application and testing the upload endpoint.

Main topics:

- `UploadFile`
- `File(...)`
- `bytes`
- `multipart/form-data`
- `python-multipart`
- cURL
- `curl -F`
- `@filename`
- Swagger UI
- Swagger vs cURL
- File-upload request flow
- Reading uploaded files
- Converting bytes to text

---

# 2. What is a file upload?

A file upload happens when a client sends a file from the client machine to a server.

Example:

```text
My Computer
    |
    | hr_policy.txt
    v
HTTP Request
    |
    | multipart/form-data
    v
FastAPI Server
    |
    v
UploadFile


SpooledTemporaryFile = a temporary file-like storage area that Python uses to hold uploaded file data, using memory for smaller data and potentially disk for larger data.

### Question 1: What is a `SpooledTemporaryFile`?

**Answer:**
A `SpooledTemporaryFile` is a **temporary file used by Python to store uploaded file data while your program is working with it**.

---

### Question 2: Why is it called "temporary"?

**Answer:**
Because it is used temporarily while the application processes the uploaded file. You don't normally need to manually create a permanent file just to receive the upload.

---

### Question 3: Why is it called "spooled"?

**Answer:**
Because smaller data can be kept in **memory**, and when the data gets larger, it can be **spooled to disk**.

```text
Small file  → Memory
Large file  → Disk
```

---

### Question 4: Where do I see it in FastAPI?

**Answer:**

```python
file.file
```

When `file` is an `UploadFile`, `file.file` is the underlying `SpooledTemporaryFile`.

```text
UploadFile
    │
    └── file
         ↓
   SpooledTemporaryFile
```

---

### Question 5: Is `SpooledTemporaryFile` the same as `bytes`?

**Answer:**
**No.**

```text
file.file
   ↓
SpooledTemporaryFile
   ↓
File-like object
```

Whereas:

```python
content = await file.read()
```

gives:

```text
content
   ↓
bytes
```

---

### Question 6: What is the easiest way to remember it?

**Answer:**

> **`file.file` = the temporary file object**
> **`await file.read()` = the actual file data as bytes**
