import test_function


SM = 'smiles'
INC = 'inchi'


print("\n\nЭто странная соль-стероид")
test_function.check("InChI=1S/C19H29O5P.Fe.2H2O/c1-18-7-5-11(20)9-15"
                    "(18)16(25(22,23)24)10-12-13-3-4-17(21)19(13,2)8-6"
                    "-14(12)18;;;/h9,12-14,16-17,21H,3-8,10H2,1-"
                    "2H3,(H2,22,23,24);;2*1H2/q;+2;;/p-2/t12-,13-"
                    ",14-,16?,17-,18+,19-;;;/m0.../s1", INC)
test_function.check("[Fe+2].O.O.[O-]P([O-])(=O)C1C[C@H]2[C@@H]3CC[C@H]"
                    "(O)[C@@]3(C)CC[C@@H]2[C@@]2(C)CCC(=O)C=C12", SM)

print("\n\nЭто бензол")
test_function.check("c1ccccc1", SM)
test_function.check("InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H", INC)

print("\n\nЭто сульфат меди")
test_function.check("InChI=1S/Cu.H2O4S/c;1-5(2,3)4/h;(H2,1,2,3,4)/q+2;/p-2",
                    INC)
test_function.check("[Cu+2].[O-]S([O-])(=O)=O", SM)


print("\n\nЭто водород")
test_function.check("[HH]", SM)
test_function.check("InChI=1S/H2/h1H", INC)

print("\n\nЭто перекись водорода")
test_function.check("OO", SM)
test_function.check("InChI=1S/H2O2/c1-2/h1-2H", INC)

print("\n\nЭто кислород")
test_function.check("O=O", SM)
test_function.check("InChI=1S/O2/c1-2", INC)

print("\n\nЭто кальций")
test_function.check("[Ca]", SM)
test_function.check("InChI=1S/Ca", INC)
