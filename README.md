# pracownia_elektrony

## Ścieżka do zmierzonych danych
W module `load_file` należy ustawić ścieżkę do katalogu zawierającego pliki pomiarów.

Wewątrz tego folderu powinny znajdować się inne katalogi o nazwach:
- rozpoczynających się od `13_` lub `23_`
- następnie zawierających wartość napięcia dryfu w Voltach
- w razie potrzeby zawierających dowolny ciąg znaków po kolejnym znaku `_` (nieobowiązkowo).

 Katalogi kończące się sekwencją `png` są ignorowane.
 
 W każdym z nieignorowanych katalogów powinny znaleźć się pliki, z których każdy jest zapisanym za pomocą oscyloskopu pomiarem.
 
 ## Ścieżka zapisania danych
 Aby zapisać przetworzone dane, należy uzupełnić ścieżkę zapisu w module `resultbuilder`
