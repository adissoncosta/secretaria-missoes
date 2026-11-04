# Remove dados pessoais (RG, CPF, nascimento, endereço, contatos) antes de publicar no GitHub.
# Uso: python3 sanitize.py <pasta com edicoes/*.json> <saida edicoes.json>
import json,re,sys,glob,os
SENS={'rg','cpf','nasc','nascConj','endereco','bairro','cep','telefone','celular','email','emailAnt','profissao','naturalidade','enderecoDoConj','by'}
PAT=[re.compile(r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}'),re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+'),re.compile(r'\(?\d{2,3}\)?\s?9?\d{4}-\d{4}')]
def scrub(o):
    if isinstance(o,dict):
        r={k:scrub(v) for k,v in o.items() if k not in SENS}
        if 'cep' in o: r['_cep69']=str(o.get('cep') or '').replace('.','').startswith('69')
        return r
    if isinstance(o,list): return [scrub(x) for x in o]
    if isinstance(o,str):
        for p in PAT: o=p.sub('[dado removido]',o)
    return o
if __name__=='__main__':
    src,dst=sys.argv[1],sys.argv[2]
    ovr={}
    for f in sorted(glob.glob(os.path.join(src,'edicoes','*.json'))):
        d=json.load(open(f)); k=os.path.basename(f)[:-5]
        ovr[k]={'kind':d.get('kind'),'nome':d.get('nome'),'fields':scrub(d.get('fields') or {}),'updatedAt':d.get('updatedAt'),'conferir':scrub(d.get('conferir') or [])}
    json.dump(ovr,open(dst,'w'),ensure_ascii=False,indent=1,sort_keys=True)
    print(len(ovr),'edições')
