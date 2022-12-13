
# Examples: 

# Collect links for "some keyword":


```python3 cutecollect.py "some keyword"```



# Collect links for keywords inside the list.txt file


```python3 cutecollect.py list.txt```



# Collect links with keyword list and footprints list


```python3 cutecollect.py list.txt -f footprints.txt```



# Collect links with keyword list and footprints list for gov. top level domain


```python3 cutecollect.py list.txt -f footprints.txt -e "site:gov"```



# Collect links with keyword list and footprints list for gov. top level domain with bruteforcing using tor as a proxy


```python3 cutecollect.py list.txt -f footprints.txt -e "site:gov" -b --tor```



# Collect links with keyword list and footprints list for gov. top level domain with randomization using tor as a proxy


```python3 cutecollect.py list.txt -f footprints.txt -e "site:gov" -r --tor```
