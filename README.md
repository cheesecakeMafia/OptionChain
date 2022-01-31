# OptionChain

Using the nseindia.com/ to scrape the option chains of various securities into pandas dataframes and doing some basic manipulations like plotting skew and term structure.

## Run locally

```sh
git clone https://github.com/Cheesecake-mafia/OptionChain.git
# or clone your own fork

cd OptionChain
```
</br>

```py
import requests
import pandas as pd
import matplotlib.pyplot as plt

```
</br>

## Input the symbol of the security whose option chain you want

```py

security = input("For what security do you want an option chain?\n")
```

## Just run the rest of the code in either jupyter notebook or any IDE of your choice and it will do the rest.
