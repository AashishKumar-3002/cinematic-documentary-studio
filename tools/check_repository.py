"""Check the Git publication set without reading ignored personal files or exposing secret values."""
import ast
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def main():
    result=subprocess.run(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT,capture_output=True,check=True)
    paths=sorted(set(p for p in result.stdout.decode('utf-8').split('\0') if p))
    forbidden={'.venv','.research-venv','node_modules','.cache','models','credentials','learned','reference','research','__pycache__','.thumbnails','.waveform-cache'}
    secrets=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'\b(?:ghp|gho|ghu|ghs)_[A-Za-z0-9]{30,}\b',r'\bgithub_pat_[A-Za-z0-9_]{40,}\b',r'\bAIza[A-Za-z0-9_-]{35}\b']
    errors=[];total=0;python_count=0
    for rel in paths:
        path=ROOT/rel;parts=Path(rel).parts
        if not path.is_file():continue
        if forbidden.intersection(parts) or (parts[0]=='projects' and {'audio','out','assets','fonts','release'}.intersection(parts)):
            errors.append(f'Excluded runtime/private directory in publication set: {rel}')
        if path.suffix.lower() in {'.mp4','.wav','.m4a','.onnx','.bin','.exe','.dll','.pdf','.pyc'}:
            errors.append(f'Generated/binary/reference file in publication set: {rel}')
        size=path.stat().st_size;total+=size
        if size>5*1024*1024:errors.append(f'File exceeds 5 MB source-publication limit: {rel}')
        if path.suffix.lower() in {'.py','.md','.json','.ps1','.sh','.zsh','.txt','.yml','.yaml','.html'} or path.name in {'LICENSE','.gitignore','.gitattributes'}:
            text=path.read_text(encoding='utf-8-sig')
            if any(re.search(pattern,text) for pattern in secrets):errors.append(f'Possible embedded credential: {rel} (value withheld)')
            if path.suffix in {'.sh','.zsh'} and b'\r' in path.read_bytes():errors.append(f'Unix shell script needs LF line endings: {rel}')
            if path.suffix=='.py':
                try:ast.parse(text,filename=rel);python_count+=1
                except SyntaxError as exc:errors.append(f'Python syntax: {rel}:{exc.lineno}')
            if path.suffix=='.json':
                try:json.loads(text)
                except json.JSONDecodeError as exc:errors.append(f'JSON syntax: {rel}:{exc.lineno}')
    print(f'Publication set: {len(paths)} files, {total/1024/1024:.2f} MB; {python_count} Python files checked')
    if errors:
        print('\n'.join(errors));return 1
    print('PASS: syntax/JSON, file-size rules, excluded-directory rules and credential-pattern check')
    print('This is a targeted publication check, not a guarantee that every secret format is detectable.')
    return 0

if __name__=='__main__':raise SystemExit(main())
