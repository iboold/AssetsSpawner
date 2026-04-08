# 🧩 Asset Spawner - Import GTAV Assets (Blender Addon)

## 📌 Description

**Asset Spawner** is a Blender addon designed to quickly import GTA V assets (`.ydr` / `.yft`) using a simple name search.

It can also **optionally** auto-apply textures from game files, but textures are **NOT required** for basic usage.

---

## 🚀 Features

* 🔍 **Smart Search** – Find assets instantly by name
* 📦 **Fast Import** – Direct import via Sollumz
* 🎨 **Optional Auto Texture Finder (DDS)** – Automatically matches and applies textures *(optional)*
* ⚡ **Multithreaded Texture Loading** – Prevents UI freezing
* 👻 **Hide Collisions** – Automatically hides collision meshes
* 🧠 **Clean UI** – Simple and intuitive sidebar panel

---

## 🛠️ Requirements

* Blender 5.0+
* **Sollumz** addon installed
* GTA V game files (Models required, Textures optional)
* You MUST use at least an **SSD**
  
---

## 📦 Extracting GTA V Assets (Required)

Before using this addon, you must extract GTA V assets using **CodeWalker**.

---

### 🛠️ Step 1: Extract Models (.ydr / .yft)

1. Open **CodeWalker**

2. From the top-right menu, go to:

   ```
   Tools → Extract Raw Files
   ```

3. Set your **Output Folder** (where models will be saved)

4. In **File Match**, type:

   ```
   .ydr
   ```

5. Make sure:

   * ✅ set to **Ends With**
   * ✅ **Compress Files** is enabled

6. Click **Extract** and wait until it finishes

7. After extraction:

   * Rename file mach from:

     ```
     .ydr → .yft
     ```
8. Click **Extract** and wait until it finishes

👉 You can now use the addon normally (models only, no textures needed 'only embedded textures will appear').

⚠️ **Storage Required:** ~28GB free space

---

### 🎨 Step 2: Extract Textures (.dds) *(Optional)*

⚠️ **This step is completely optional.**
You only need this if you want automatic texture assignment inside Blender.

1. Open **CodeWalker**

2. Go to:

   ```
   Tools → Extract Textures
   ```

3. Choose a **different Output Folder** (NOT the same as models)

4. Set:

   * Texture Type → **YTD only**

5. Click **Extract**

⚠️ **Storage Required:** ~61GB free space

---

## ⚡ Performance Tip (Very Important)

* You MUST use at least an **SSD**
* ⚡ Recommended: **M.2 SSD**

This is important to:

* Avoid extremely slow extraction times in CodeWalker
* Ensure smooth performance inside Blender

---

## 📥 Installation

1. Download the addon as a `.zip` file
2. Open Blender
3. Go to:

   ```
   Edit → Preferences → Add-ons → Install
   ```
4. Select the addon file
5. Enable the addon ✔

---

## ⚙️ Setup (Important)

Before using the addon, configure the folders:

* 📁 **Assets Folder** → Path to `.ydr / .yft` files *(Required)*
* 🎨 **Textures Folder** → Path to `.dds` files *(Optional)*

Access settings via:

```
Edit → Preferences → Add-ons → Asset Spawner
```

---

## ▶️ Usage

1. Open:

   ```
   View3D → Sidebar → Asset Spawner (Press N)
   ```

2. Enter the object name in:

   ```
   Object Name
   ```

3. Optional settings:

   * ✅ **Find Textures** → Apply textures automatically *(only if textures folder is set)*
   * ✅ **Hide Collisions** → Hide collision meshes

4. Click:

   ```
   Import Object
   ```

---

## 🧠 How It Works

* Searches the assets folder for matching `.ydr` or `.yft` files
* Imports the first match using Sollumz
* If **Find Textures** is enabled:

  * Scans materials and texture nodes
  * Matches texture names with `.dds` files
  * Applies textures automatically
* Texture loading runs in a separate thread to keep Blender responsive

---

## ⚡ Performance

* Uses **multithreading** to avoid freezing during texture loading
* Optimized for large asset libraries

---

## 🐞 Known Issues

* Texture names must match correctly for auto-detection
* Sollumz must be installed for importing to work
* Only `.dds` textures are supported

---

## 📂 Supported Formats

* Models: `.ydr`, `.yft`
* Textures: `.dds` *(optional)*

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome 🙌

---

## 📜 License

MIT License
