"""Conservative FTB SNBT draft merge. Preserves local IDs; reports conflicts.

No Minecraft paths, downloads, or installation. Output always requires review.
The parser supports the SNBT subset used by FTB quest files; unknown syntax fails.
"""
from dataclasses import dataclass
import json
import re

@dataclass(frozen=True)
class Atom:
    raw: str

@dataclass
class TypedArray:
    kind: str
    values: list

TOKEN = re.compile(r'\s+|//[^\n]*|\#[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[{}\[\]:,;]|[^\s{}\[\]:,;"\']+')

def parse(text,identical_duplicates=None,*,last_wins=False):
    tokens=[]
    end=0
    for found in TOKEN.finditer(text.lstrip('\ufeff')):
        if found.start()!=end: raise ValueError(f'Unsupported SNBT at {end}')
        end=found.end()
        token=found.group()
        if not token.isspace() and not token.startswith(('//','#')): tokens.append(token)
    if end!=len(text.lstrip('\ufeff')): raise ValueError('Trailing unsupported SNBT')
    position=0
    def take():
        nonlocal position
        if position>=len(tokens): raise ValueError('Unexpected end of SNBT')
        token=tokens[position]
        position+=1
        return token
    def peek(): return tokens[position] if position<len(tokens) else None
    def string(token):
        if token.startswith('"'): return json.loads(token)
        if token.startswith("'"):
            return re.sub(r"\\(['\\])",r'\1',token[1:-1])
        return token
    def value():
        token=take()
        if token=='{':
            result={}
            while peek()!='}':
                key=string(take())
                if take()!=':': raise ValueError('Missing key separator')
                child=value()
                if key in result:
                    if identical_duplicates is None or (result[key]!=child and not last_wins):
                        raise ValueError(f'Duplicate SNBT key: {key}')
                    identical_duplicates.append(key if result[key]==child else {'key':key,'previous':dump(result[key]),'selected':dump(child)})
                result[key]=child
                if peek()==',': take()
            take()
            return result
        if token=='[':
            kind=None
            if peek() in ('I','B','L') and position+1<len(tokens) and tokens[position+1]==';':
                kind=take()
                take()
            result=[]
            while peek()!=']':
                result.append(value())
                if peek()==',': take()
            take()
            return TypedArray(kind,result) if kind else result
        if token.startswith(('"',"'")): return string(token)
        if token in '{}[]:,;': raise ValueError(f'Unexpected token: {token}')
        return Atom(token)
    result=value()
    if position!=len(tokens): raise ValueError('Extra tokens after root')
    return result

def dump(value,depth=0):
    if isinstance(value,Atom): return value.raw
    if isinstance(value,TypedArray): return '['+value.kind+'; '+', '.join(dump(v) for v in value.values)+']'
    if isinstance(value,str): return json.dumps(value,ensure_ascii=False)
    indent='\t'*depth
    if isinstance(value,dict):
        return '{\n'+'\n'.join(indent+'\t'+json.dumps(k,ensure_ascii=False)+': '+dump(v,depth+1) for k,v in value.items())+'\n'+indent+'}'
    if isinstance(value,list): return '[\n'+'\n'.join(indent+'\t'+dump(v,depth+1) for v in value)+'\n'+indent+']'
    raise TypeError(type(value))

MISSING=object()

def identity(value):
    if isinstance(value,str) and value and ':' not in value: return value
    if isinstance(value,Atom) and re.fullmatch('[0-9A-Fa-f]{16}',value.raw): return value.raw
    return None

def keyed(values):
    return isinstance(values,list) and bool(values) and all(isinstance(v,dict) and identity(v.get('id')) is not None for v in values)

def has_ids(value):
    if isinstance(value,dict): return identity(value.get('id')) is not None or any(has_ids(v) for v in value.values())
    return isinstance(value,list) and any(has_ids(v) for v in value)

def validate(value):
    if isinstance(value,dict):
        for child in value.values(): validate(child)
    if isinstance(value,list):
        found=[identity(v.get('id')) for v in value if isinstance(v,dict) and identity(v.get('id')) is not None]
        if found and len(found)!=len(value): raise ValueError('Mixed identity and unidentified entries require review')
        if len(set(found))!=len(found): raise ValueError('Duplicate quest IDs in list')
        for child in value: validate(child)

def merge(base,upstream,local,conflicts,path=''):
    for value in (base,upstream,local): validate(value)
    return _merge(base,upstream,local,conflicts,path)

def _merge(b,u,l,notes,path):
    if u is MISSING:
        if l is not MISSING and b is not MISSING:
            notes.append({'path':path,'kind':'upstream_removal_preserved'})
        return l
    if l is MISSING and b is not MISSING:
        if u!=b: notes.append({'path':path,'kind':'local_deletion_preserved'})
        return MISSING
    if l is not MISSING and type(u)!=type(l) and has_ids(l):
        notes.append({'path':path,'kind':'identity_container_type_change_preserved'})
        return l
    if path.endswith('/id') and identity(l) is not None and identity(u)!=identity(l):
        notes.append({'path':path,'kind':'identity_change_preserved'})
        return l
    if b is MISSING and isinstance(u,dict) and isinstance(l,dict) and u!=l and identity(l.get('id')) is not None:
        notes.append({'path':path,'kind':'unknown_baseline_identity_conflict'})
        return l
    if isinstance(u,dict) and (l is MISSING or isinstance(l,dict)):
        old=b if isinstance(b,dict) else {}
        ours=l if isinstance(l,dict) else {}
        result={}
        for key in dict.fromkeys([*ours,*u]):
            child=_merge(old.get(key,MISSING),u.get(key,MISSING),ours.get(key,MISSING),notes,path+'/'+key)
            if child is not MISSING: result[key]=child
        return result
    lists=[v for v in (b,u,l) if v is not MISSING]
    if lists and all(isinstance(v,list) and (not v or keyed(v)) for v in lists) and any(keyed(v) for v in lists):
        old={identity(v['id']):v for v in b} if isinstance(b,list) else {}
        theirs={identity(v['id']):v for v in u}
        ours={identity(v['id']):v for v in l} if isinstance(l,list) else {}
        result=[]
        for key in dict.fromkeys([*ours,*theirs]):
            child=_merge(old.get(key,MISSING),theirs.get(key,MISSING),ours.get(key,MISSING),notes,path+'/'+key)
            if child is not MISSING: result.append(child)
        return result
    if l is MISSING: return u
    if l==u or u==b: return l
    if l==b: return u
    notes.append({'path':path,'kind':'both_changed_keep_local','base':None if b is MISSING else dump(b),'upstream':dump(u),'local':dump(l)})
    return l
