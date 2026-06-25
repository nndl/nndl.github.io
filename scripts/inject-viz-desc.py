#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-shot: give every viz/*.md a unique SEO `description` in its front matter.

Source of truth is the hand-written `blurb=` on each card in viz/index.md (the
same one-liners shown under each card). Pages without a card fall back to their
first prose paragraph. Re-runnable: pages that already have a description are
left untouched.
"""
import re, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

idx = open('viz/index.md', encoding='utf-8').read()
blocks = re.findall(r'\{%\s*include viz-card\.html(.*?)%\}', idx, re.S)
slug2blurb = {}
for b in blocks:
    u = re.search(r'url="([^"]+)"', b)
    bl = re.search(r'blurb="([^"]+)"', b)
    if not u or not bl:
        continue
    m = re.match(r'/viz/([^/]+)/?$', u.group(1))
    if m:
        slug2blurb[m.group(1)] = bl.group(1).strip()
print('card blurbs mapped to local slugs:', len(slug2blurb))


def esc(s):
    return s.replace(chr(92), chr(92) * 2).replace('"', chr(92) + '"')


def first_para(body):
    for line in body.splitlines():
        t = line.strip()
        if not t or t[0] in '#<{->|`*!':
            continue
        t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
        t = re.sub(r'[*_`]', '', t)
        if len(t) >= 10:
            return t[:118]
    return None


from_blurb = fallback = skipped = had = 0
for path in glob.glob('viz/*.md'):
    slug = os.path.basename(path)[:-3]
    src = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', src, re.S)
    if not m:
        skipped += 1
        continue
    fm, body = m.group(1), m.group(2)
    if re.search(r'^description:', fm, re.M):
        had += 1
        continue
    if slug == 'index':
        desc = '书中关键概念与模型的动图与交互演示，按《神经网络与深度学习》章节顺序排列，便于直观理解。'
    elif slug in slug2blurb:
        desc = slug2blurb[slug]
        from_blurb += 1
    else:
        fp = first_para(body)
        if not fp:
            skipped += 1
            continue
        desc = fp
        fallback += 1
    lines = fm.split('\n')
    out, inserted = [], False
    for ln in lines:
        out.append(ln)
        if not inserted and ln.startswith('title:'):
            out.append('description: "' + esc(desc) + '"')
            inserted = True
    if not inserted:
        out.insert(1, 'description: "' + esc(desc) + '"')
    open(path, 'w', encoding='utf-8', newline='\n').write('---\n' + '\n'.join(out) + '\n---\n' + body)

print('injected from blurb:', from_blurb)
print('injected from first paragraph:', fallback)
print('already had description:', had)
print('skipped (no front matter / no text):', skipped)
