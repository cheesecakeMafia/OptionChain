# OptionChain

Used the nseindia.com/ to scrape the option chains of various securities into dictionary of pandas dataframes and doing some basic manipulations like plotting skew and term structure curves.

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

## Input the asset class and the symbol of the security whose option chain you want

```py
asset_class = input("What asset class do you want? Equities or Index\n")
security = input("For what security do you want an option chain?\n")
```

## Just run the rest of the code in either jupyter notebook or any IDE of your choice and it will do the rest.
