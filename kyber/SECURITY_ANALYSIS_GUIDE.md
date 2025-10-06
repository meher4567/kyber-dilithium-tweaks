# Kyber Security Analysis Guide

Complete guide for running security validation on your Kyber implementations.

---

## 📋 Overview

This security analysis validates that your parameter modifications maintain acceptable security levels against known lattice attacks (classical and quantum).

**What it does:**
- Analyzes all 4 parameter configurations
- Tests against Primal and Dual attacks
- Calculates Core-SVP hardness
- Generates thesis-ready tables

---

## 🚀 Quick Start (Fedora)

### Step 1: Install Prerequisites

```bash
# Install system dependencies
sudo dnf install python3 python3-pip git

# Verify installation
python3 --version
pip3 --version
git --version