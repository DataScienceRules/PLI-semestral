# PLI-semestral

Semestrální práce z předmětu Úvod do počítačové lingvistiky

Program vytváří znakový, pravěpodobnostní trigram a vyhlazuje ho metodou witten-bell.
Trigramy jsou natrénovány na české a slovenské wikipedii. Uloženy jsou ve formátu JSON.
Trigramy jsou testovány na přiložených textech.

Výsledky testů
A) Plná abeceda

  1) úryvky z diplomových prací
  
  DPtextcz
  
  CZ  1.9098168889242554e+266
  
  SK  inf
  
  DPtextsk
  
  CZ  inf
  
  SK  inf
  
  2) krátké články z hospodářských novin
  
  HNtext
  
  CZ  inf
  
  SK  inf
  
  HNtextsk
  
  CZ  1.1408317299693401e+213
  
  SK  3.1591679913380422e+190

  3) několik slov které jsou pro oba jazyky totožké
  czskidentity

B) Redukovaná abeceda
