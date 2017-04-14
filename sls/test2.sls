cpfile:
  file.recurse:
    - name: d:\data
    - makedirs: Ture
    - source: salt://data
    - clean: True
    - include_empty: True
