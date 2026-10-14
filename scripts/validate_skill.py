"""Structural diagnostic; does not assess requirement semantics or model behavior."""
import json
import re
import sys
from pathlib import Path
import yaml


def check(root):
    root = Path(root).resolve()
    errors = []
    entry = root / 'SKILL.md'
    metadata = root / 'agents/openai.yaml'
    if not entry.is_file():
        return {'status': 'fail', 'errors': ['SKILL.md missing']}
    text = entry.read_text(encoding="utf-8")
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    try:
        front = yaml.safe_load(match.group(1)) if match else {}
        if front.get('name') != root.name:
            errors.append('Skill frontmatter name differs from directory')
        if not isinstance(front.get('description'), str) or not front['description'].strip():
            errors.append('Missing frontmatter description')
        ui = yaml.safe_load(metadata.read_text(encoding="utf-8"))['interface']
        if not 25 <= len(ui['short_description']) <= 64:
            errors.append('UI short_description length outside 25..64')
        if '$' + front.get('name', '') not in ui['default_prompt']:
            errors.append('UI default_prompt does not invoke skill')
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        errors.append('Invalid YAML/metadata: ' + str(exc))
    graph = {}
    link_count = 0
    mds = sorted(root.rglob('*.md'))
    for file in mds:
        contents = file.read_text(encoding="utf-8")
        graph[file.resolve()] = []
        if '[TODO:' in contents:
            errors.append(f'Initializer placeholder in {file.relative_to(root)}')
        fence = None
        for line in contents.splitlines():
            opener = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
            if not opener:
                continue
            marker, rest = opener.groups()
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not rest.strip():
                fence = None
        if fence:
            errors.append(f'Unclosed code fence in {file.relative_to(root)}')
        for target in re.findall(r'\]\(([^)]+)\)', contents):
            if '://' in target or target.startswith('#'):
                continue
            dest = (file.parent / target.split('#')[0]).resolve()
            link_count += 1
            if not dest.is_file():
                errors.append(f'Broken link: {file.relative_to(root)} -> {target}')
            else:
                graph[file.resolve()].append(dest)
    reached = set()
    pending = [entry.resolve()]
    while pending:
        current = pending.pop()
        if current in reached:
            continue
        reached.add(current)
        pending.extend(graph.get(current, []))
    for ref in root.glob('references/*.md'):
        if ref.resolve() not in reached:
            errors.append(f'Undiscoverable reference: {ref.name}')
    return {'status':'fail' if errors else 'pass','markdown_files':len(mds),'local_links':link_count,'references_reachable':len(list(root.glob('references/*.md'))),'errors':errors}


if __name__ == '__main__':
    result = check(sys.argv[1])
    print(json.dumps(result, indent=2))
    sys.exit(1 if result['errors'] else 0)
