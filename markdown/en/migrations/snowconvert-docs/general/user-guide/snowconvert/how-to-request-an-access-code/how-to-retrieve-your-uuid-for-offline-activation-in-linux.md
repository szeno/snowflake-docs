# SnowConvert AI - How to Retrieve Your UUID for Offline Activation in Linux

SnowConvert AI requires a **UUID** to validate the license for offline activation in Linux. Follow these steps to find and provide the UUID:

## **Step 1: Open a Terminal**

To begin, open a terminal on your Linux system by:

- Pressing **Ctrl + Alt + T**
- Searching for **“Terminal”** in your application menu

## **Step 2: Retrieve the UUID of the Root Device**

You need to obtain the **UUID** of your root device. Try the following commands in the given order until you get a valid UUID.

### **Option 1: Primary Command**

Run the following command first:

Copy code

```
findmnt / -o UUID -n
```

If successful, it will return a UUID similar to this:

Copy code

```
5a14ccf7-6bac-47b7-a3d6-6c10822fb10d
```

### **Option 2: Alternative Command (If Option 1 Fails)**

If the first command does not return a UUID in a single line, try:

Copy code

```
blkid -s UUID -o value $(findmnt -n -o SOURCE /)
```

Expected output:

Copy code

```
5a14ccf7-6bac-47b7-a3d6-6c10822fb10d
```

### **Option 3: Last Resort (If the Previous Commands Fail)**

If neither of the above commands work, use:

Copy code

```
lsblk -nro UUID
```

This must return **only one UUID**. If multiple UUIDs are listed, this method **will not work**. Ensure that the output contains a **single valid UUID**, or try one of the previous methods again.

## **Step 3: Send the UUID**

Once you have retrieved the correct UUID, copy it and send it to the **SnowConvert AI support team** for activation.
