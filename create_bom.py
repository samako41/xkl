#!/usr/bin/env python3
"""
create_bom.py  –  import vertical BoMs into Odoo from an ICIT‑style CSV

Usage
-----
python create_bom.py \
       --url http://localhost:8100 \
       --db  odoo18 \
       --user admin \
       --password admin \
       --csv "Bom for icit.csv" \
       --first-level 0      # 0 = auto‑detect first populated L‑column
"""

import argparse
import csv
import re
import sys
import unicodedata
import xmlrpc.client
from collections import defaultdict
from pathlib import Path

# ─────────────── helpers ────────────────

LEVEL_RE = re.compile(r"^L(\d+)$", re.IGNORECASE)
PRODUCT_CACHE, TEMPLATE_CACHE = {}, {}


def normalise(text: str) -> str:
    """Trim + replace NB‑spaces → normal spaces."""
    if text is None:
        return ""
    text = unicodedata.normalize("NFKC", text)
    return text.replace("\u00A0", " ").strip()


def detect_columns(headers, first_level):
    level_cols, qty_col = {}, None
    for raw in headers:
        h = normalise(raw)
        if h.lower().startswith("qty"):
            qty_col = raw
            continue
        m = LEVEL_RE.match(h)
        if m:
            level_cols[int(m.group(1))] = raw

    if qty_col is None:
        sys.exit("No Qty column found.")
    if first_level is None:
        first_level = min(level_cols)          # auto‑detect (L3 in your file)

    # keep only levels ≥ first_level
    level_cols = {lvl: col for lvl, col in level_cols.items()
                  if lvl >= first_level}
    if not level_cols:
        sys.exit(f"✖  No L‑columns at or below L{first_level}.")
    return level_cols, qty_col, first_level


# ─────────────── Odoo RPC ────────────────

def connect_odoo(url, db, user, pwd):
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", allow_none=True)
    uid = common.authenticate(db, user, pwd, {})
    if not uid:
        sys.exit("✖  Invalid URL / DB / credentials.")
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", allow_none=True)
    return uid, models


def get_or_create_product(models, db, uid, pwd, code):
    code = code.strip()
    if not code:
        return None
    if code in PRODUCT_CACHE:
        return PRODUCT_CACHE[code]

    prod = models.execute_kw(db, uid, pwd, "product.product", "search",
                             [[["default_code", "=", code]]], {"limit": 1})
    if prod:
        PRODUCT_CACHE[code] = prod[0]
        return prod[0]

    tmpl_id = models.execute_kw(db, uid, pwd, "product.template", "create",
                                [{"name": code, "default_code": code,
                                  "type": "consu", "purchase_ok": True,
                                  "sale_ok": False}])
    var_id = models.execute_kw(db, uid, pwd, "product.template", "read",
                               [tmpl_id], {"fields": ["product_variant_id"]})[0]["product_variant_id"][0]
    PRODUCT_CACHE[code] = var_id
    TEMPLATE_CACHE[code] = tmpl_id
    print(f"🟢  Created product {code}")
    return var_id


def get_template(models, db, uid, pwd, code):
    if code in TEMPLATE_CACHE:
        return TEMPLATE_CACHE[code]
    prod = PRODUCT_CACHE.get(code)
    if not prod:
        return None
    tmpl_id = models.execute_kw(db, uid, pwd, "product.product", "read",
                                [prod], {"fields": ["product_tmpl_id"]})[0]["product_tmpl_id"][0]
    TEMPLATE_CACHE[code] = tmpl_id
    return tmpl_id


def create_bom(models, db, uid, pwd, parent_code, child_lines):
    tmpl_id = get_template(models, db, uid, pwd, parent_code)
    if not tmpl_id:
        return

    exists = models.execute_kw(db, uid, pwd, "mrp.bom", "search",
                               [[["product_tmpl_id", "=", tmpl_id]]], {"limit": 1})
    if exists:
        print(f"BoM already exists for {parent_code}")
        return

    merged = defaultdict(float)
    for pid, qty in child_lines:
        merged[pid] += qty

    bom_lines = [(0, 0, {"product_id": pid, "product_qty": qty})
                 for pid, qty in merged.items()]
    models.execute_kw(db, uid, pwd, "mrp.bom", "create",
                      [{"product_tmpl_id": tmpl_id,
                        "type": "normal",
                        "code": f"BOM-{parent_code}",
                        "bom_line_ids": bom_lines}])
    print(f"Created BoM  {parent_code}")


# ─────────────── CSV → tree ───────────────

def parse_csv(csv_path: Path, first_level=None, max_level=20):
    with csv_path.open(newline="", encoding="utf‑8‑sig") as f:
        rdr = csv.DictReader(f)
        level_cols, qty_col, first_level = detect_columns(rdr.fieldnames, first_level)

        tree, stack = defaultdict(list), {}
        for row in rdr:
            qty = float(normalise(row.get(qty_col))) if normalise(row.get(qty_col)) else 1.0

            # step: find first non‑empty Lx cell → parent at that level
            for lvl in range(first_level, max_level + 1):
                col = level_cols.get(lvl)
                if not col:
                    continue
                val = normalise(row.get(col))
                if val:
                    stack[lvl] = val
                    # drop deeper parents
                    for deeper in range(lvl + 1, max_level + 1):
                        stack.pop(deeper, None)
                    break

            # step: for every parent in the stack, look one level deeper
            for lvl, parent in list(stack.items()):
                child_col = level_cols.get(lvl + 1)
                if not child_col:
                    continue
                child_val = normalise(row.get(child_col))
                if child_val:
                    tree[parent].append((child_val, qty))
        return tree


# ─────────────── main ───────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--db", required=True)
    ap.add_argument("--user", required=True)
    ap.add_argument("--password", required=True)
    ap.add_argument("--csv", required=True, type=Path)
    ap.add_argument("--first-level", type=int, default=3,
                    help="First L‑column to treat as a parent "
                         "(0 = auto‑detect, default 3).")
    args = ap.parse_args()

    first_level = None if args.first_level == 0 else args.first_level
    bom_tree = parse_csv(args.csv, first_level)

    if not bom_tree:
        sys.exit("Parsed zero parents – please check the CSV layout.")

    print(f"Parsed {len(bom_tree):,} parents")

    uid, models = connect_odoo(args.url, args.db, args.user, args.password)
    pwd = args.password

    # create / fetch all products
    for parent, children in bom_tree.items():
        get_or_create_product(models, args.db, uid, pwd, parent)
        for child, _ in children:
            get_or_create_product(models, args.db, uid, pwd, child)

    # create BoMs
    for parent, children in bom_tree.items():
        create_bom(models, args.db, uid, pwd,
                   parent,
                   [(PRODUCT_CACHE[child], qty) for child, qty in children])

    print("Vertical BoM import complete.")


if __name__ == "__main__":
    main()
