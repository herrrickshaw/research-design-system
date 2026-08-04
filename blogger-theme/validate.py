#!/usr/bin/env python3
"""Validate the Blogger theme. Run after every edit."""
import re, sys, xml.etree.ElementTree as ET
src = open('masaladeutsch.xml', encoding='utf-8').read()
fails = []
try:
    ET.fromstring(src.replace('<!DOCTYPE html>', ''))
except Exception as e:
    fails.append(f"XML not well-formed: {e}")
cda = [m.span() for m in re.finditer(r'<!\[CDATA\[.*?\]\]>', src, re.S)]
inc = lambda i: any(a <= i < b for a, b in cda)
for m in re.finditer(r'<!--(.*?)-->', src, re.S):          # '--' inside a comment is illegal XML
    if not inc(m.start()) and '--' in m.group(1):
        fails.append(f"illegal '--' in XML comment: {' '.join(m.group(1).split())[:50]}")
clean = re.sub(r'<!--.*?-->', lambda m: '' if not inc(m.start()) else m.group(0), src, flags=re.S)
for label, needle in [("b:version", "b:version='2'"), ("b namespace", "xmlns:b="),
                      ("all-head-content", "name='all-head-content'"),
                      ("b:skin", "<b:skin><![CDATA["), ("Blog widget", "type='Blog'")]:
    if needle not in src: fails.append(f"missing {label}")
index = clean.split("cond='data:blog.pageType")[1].split('<b:else/>', 1)[1].split('</b:includable>')[0]
if 'data:post.body' in index: fails.append("index branch renders post.body -- will empty the post list")
if 'data:post.snippet' not in index: fails.append("index branch missing data:post.snippet")
if '<script' in clean.lower(): fails.append("contains a <script> tag")
ext = re.findall(r'(?:src|href)=[\'"](https?://(?!www\.w3\.org|www\.google\.com/2005)[^\'"]+)', clean)
if ext: fails.append(f"external host referenced: {ext}")
slots = re.findall(r"<b:section[^>]*id='(main-top|main-bottom)'[^>]*showaddelement='yes'", clean)
if len(slots) != 2: fails.append(f"page-body gadget slots missing: {slots}")
print("\n".join("FAIL  " + f for f in fails) if fails else "PASS  all checks green")
sys.exit(1 if fails else 0)
