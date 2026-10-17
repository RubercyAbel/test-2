"""Tests de non-régression : valeurs publiées par Schnorr (exemples 2 et 3, tableau de frottement)
et SPIROL (catalogue DIN EN 16983, E = 206 000 MPa, µ = 0,3). Lancer : python3 test_belleville.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from belleville import Rondelle
def chk(nom, val, ref, tol=0.01):
    ok = abs(val-ref) <= tol*abs(ref) + 2
    print(f"{'OK ' if ok else 'ECART'} {nom:42s} calc={val:10.1f} ref={ref}")
    return ok
res=[]
# Schnorr ex.2 : 60x30.5x1.5 l0=3.5
r=Rondelle(60,30.5,1.5,3.5)
res+=[chk("Schnorr ex2 K1",r.K1*1000,688,0.002),chk("K2",r.K2*1000,1212,0.002),chk("K3",r.K3*1000,1365,0.002)]
res+=[chk("Schnorr ex2 sigmaOM a plat",r.contraintes(2.0)["OM"],-1048)]
for s,F in ((0.5,1338),(1.0,2058),(1.5,2367),(2.0,2469)): res.append(chk(f"Schnorr ex2 F(s={s})",r.effort(s),F))
# Schnorr ex.3 : 200x82x12, l0=16.6, t'=11.5
r=Rondelle(200,82,12,16.6,tp=11.5)
res+=[chk("Schnorr ex3 K1",r.K1*1000,755,0.002),chk("K2",r.K2*1000,1315,0.002),chk("K3",r.K3*1000,1541,0.002)]
res.append(chk("Schnorr ex3 K4 (x1e5)",r.K4*1e5,105374,0.0005))
res.append(chk("Schnorr ex3 sigmaOM nominal a plat",r.contraintes(4.6)["OM"],-1579))
res.append(chk("Schnorr ex3 sigma'OM reduit",r.contraintes(4.6)["OM"]*r.K4*11.5/12,-1595))
for s,F in ((1.15,66924),(2.3,127191),(3.45,182737),(4.6,235503)): res.append(chk(f"Schnorr ex3 F(s={s})",r.effort(s),F))
for s,ref in ((1.15,416),(2.3,890),(3.45,1421),(4.6,2011)):
    st=r.contraintes(s); print(f"      ex3 s={s}: sII={st['II']:.0f} sIII={st['III']:.0f}  (colonne publiee {ref})")
# SPIROL (E=206000, mu=0.3)
cases=[((40,20.4,2.25,3.15),[(0.135,1428,229,246),(0.225,2336,392,403),(0.45,4481,835,774),(0.675,6500,1328,1112)],(0.9,8456,-1595)),
       ((40,20.4,1.0,2.3),[(0.195,375,-15,261),(0.975,1017,305,1063)],(1.3,1072,-1024)),
       ((100,51,3.5,6.3),[(2.1,13070,734,1049)],(2.8,15843,-1235)),
       ((63,31,3.5,4.9),[(1.05,15025,1296,1047)],(1.4,19545,-1524))]
for (De,Di,t,l0),pts,(sp,Fp,om) in cases:
    r=Rondelle(De,Di,t,l0)
    for s,F,s2,s3 in pts:
        st=r.contraintes(s)
        res+=[chk(f"SPIROL {De}x{Di}x{t} F(s={s})",r.effort(s),F),chk("   sigma II",st["II"],s2,0.02),chk("   sigma III",st["III"],s3,0.02)]
    res+=[chk(f"SPIROL {De}x{Di}x{t} F(plat)",r.effort(sp),Fp),chk("   sigma OM",r.contraintes(sp)["OM"],om)]
# Frottement : tableau Schnorr serie A
for n,wM,wR,ref in ((1,0,0.03,3.09),(1,0,0.05,5.26),(2,0.005,0.03,3.63),(2,0.03,0.05,8.70),(3,0.005,0.03,4.17),(3,0.03,0.05,12.36)):
    res.append(chk(f"Frottement A n={n} charge % (x100)",(1/(1-wM*(n-1)-wR)-1)*1e4,ref*100,0.002))
for n,wM,wR,ref in ((1,0,0.03,-2.91),(1,0,0.05,-4.76),(2,0.005,0.03,-3.38),(2,0.03,0.05,-7.41),(3,0.03,0.05,-9.91)):
    res.append(chk(f"Frottement A n={n} decharge % (x100)",(1/(1+wM*(n-1)+wR)-1)*1e4,ref*100,0.002))
print(sum(res),"/",len(res),"OK"); sys.exit(0 if all(res) else 1)
