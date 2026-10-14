"""Fixture-specific semantic regression checks for the synthetic library package."""
from pathlib import Path
import json,re,sys

root=Path(sys.argv[1])
edge_re=re.compile(r'^\s*(\w+)(?:\[[^\]]*\]|\{[^}]*\})?\s*-->(?:\|[^|]*\|)?\s*(\w+)',re.M)
def edges(text): return set(edge_re.findall(text))
def reachable(es,start,end,removed=None):
    seen=set();pending=[start]
    while pending:
        n=pending.pop()
        if n==removed or n in seen: continue
        if n==end: return True
        seen.add(n)
        pending.extend(b for a,b in es if a==n and b!=removed)
    return False

def acyclic(es):
    nodes={n for edge in es for n in edge};visiting=set();done=set()
    def visit(n):
        if n in visiting:return False
        if n in done:return True
        visiting.add(n)
        if not all(visit(b) for a,b in es if a==n):return False
        visiting.remove(n);done.add(n);return True
    return all(visit(n) for n in nodes)

results=[]
def record(name,condition,evidence):
    results.append({'check':name,'status':'pass' if condition else 'fail','evidence':evidence})

required=['PRD.md','SRS.md','ARCHITECTURE.md','WORKFLOWS-AND-ACCESS.md','DATABASE-DESIGN.md','IMPLEMENTATION-PLAN.md','TRACEABILITY.md']
record('package-artifacts',all((root/p).is_file() and (root/p).stat().st_size for p in required),required)
broken=[]
for file in root.glob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',file.read_text(encoding="utf-8")):
        if '://' not in link and not link.startswith('#') and not (file.parent/link.split('#')[0]).is_file():broken.append([file.name,link])
record('relative-file-links',not broken,broken)
architecture=(root/'ARCHITECTURE.md').read_text(encoding="utf-8")
embedded=re.findall(r'```mermaid\s*\n(.*?)```',architecture,re.S)
missing_embeds=[p.name for p in (root/'diagrams').glob('*.mmd') if p.read_text(encoding="utf-8").strip() not in {s.strip() for s in embedded}]
record('canonical-mermaid-copy-consistency',len(embedded)==10 and not missing_embeds,{'embedded':len(embedded),'mismatches':missing_embeds})
business=edges((root/'diagrams/business.mmd').read_text(encoding="utf-8"))
record('approval-requires-librarian-action',reachable(business,'C','G') and not reachable(business,'C','G','F'),{'pending_node':'C','approval_action':'F','approved_node':'G','bypass_without_action':reachable(business,'C','G','F')})
business_text=(root/'diagrams/business.mmd').read_text(encoding="utf-8")
system_lane=re.search(r'subgraph Sistem\n(.*?)\n end',business_text,re.S).group(1)
record('workflow-system-lane-ownership',all(re.search(r'^\s*'+n+r'[\[{]',system_lane,re.M) for n in ['C','D','R','G','H','J']),{'expected_system_nodes':['C','D','R','G','H','J']})
for name in ['sequence','return']:
    seq=(root/'diagrams'/f'{name}.mmd').read_text(encoding="utf-8")
    record('service-response-chain-'+name, 'D-->>V:' not in seq and 'D-->>S:' in seq and 'S-->>V:' in seq, {'database_result_via_service':True if 'D-->>S:' in seq else False})
erd=(root/'diagrams/erd.mmd').read_text(encoding="utf-8")
entity_map={'USER_REFERENCE':'ENT-001','BOOK':'ENT-002','LOAN':'ENT-003'}
erd_fields=set()
for entity,body in re.findall(r'^\s*(\w+) \{\n(.*?)\n \}',erd,re.M|re.S):
    for line in body.strip().splitlines():
        parts=line.split()
        if len(parts)>=2:erd_fields.add(entity_map[entity]+'.'+parts[1])
dict_fields=set(re.findall(r'^\| (ENT-\d{3}\.\w+) \|',(root/'DATABASE-DESIGN.md').read_text(encoding="utf-8"),re.M))
record('erd-dictionary-field-alignment',len(erd_fields)==14 and erd_fields==dict_fields,{'erd_fields':len(erd_fields),'dictionary_fields':len(dict_fields),'missing':sorted(erd_fields-dict_fields),'extras':sorted(dict_fields-erd_fields)})
expected={('A','U1'),('A','U2'),('A','U3'),('L','U1'),('L','U4'),('L','U5'),('L','U6'),('L','U7')}
actual=edges((root/'diagrams/usecases.mmd').read_text(encoding="utf-8"))
record('usecase-map-role-associations',expected.issubset(actual),{'expected_pairs':sorted(expected),'missing':sorted(expected-actual)})
umlfile=root/'diagrams/usecases.puml'
uml=umlfile.read_text(encoding="utf-8") if umlfile.exists() else ''
record('uml-source-and-role-associations',uml.startswith('@startuml') and '@enduml' in uml and expected.issubset(edges(uml)),{'source_exists':umlfile.is_file(),'missing_pairs':sorted(expected-edges(uml)),'format_parser':'not executed'})
deps=edges((root/'diagrams/dependencies.mmd').read_text(encoding="utf-8"))
record('task-dependencies-acyclic',acyclic(deps),sorted(deps))
srs=(root/'SRS.md').read_text(encoding="utf-8")
defs=set(re.findall(r'^\| ((?:FR|NFR)-\d{3}) \|',srs,re.M)) | set(re.findall(r'^((?:BR|DATA|IF|NFR)-\d{3})\s+—',srs,re.M))
trace=(root/'TRACEABILITY.md').read_text(encoding="utf-8")
rows=set(re.findall(r'^\| ((?:FR|NFR|BR|DATA|IF)-\d{3}) \|',trace,re.M))
record('normative-requirement-traceability',len(defs)==18 and defs==rows,{'definitions':len(defs),'rows':len(rows),'missing':sorted(defs-rows),'orphans':sorted(rows-defs)})
cases=set(re.findall(r'^## AC-\d{3} / (VER-\d{3})', (root/'VERIFICATION.md').read_text(encoding="utf-8"),re.M))
record('planned-case-inventory',cases=={f'VER-{i:03d}' for i in range(1,14)},sorted(cases))
print(json.dumps(results,indent=2))
sys.exit(1 if any(r['status']=='fail' for r in results) else 0)
