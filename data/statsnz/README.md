# README

## Quickstart

The StatsNZ layers are accessed via WFS so require an API key to access the data.
To setup your API key with RiskScape, copy paste the following:

  [datafinder.stats.govt.nz]
  framework = koordinates
  hostname = datafinder.stats.govt.nz
  api-key = TODO_YOUR_KEY_HERE

and add it to your secrets.ini file.
Replace the `TODO_YOUR_KEY_HERE` with your datafinder.stats.govt.nz API key.
You can access or create an API key at: https://datafinder.stats.govt.nz/my/api

**Tip**: A Windows user could edit their secrets file by entering the following into a command prompt:
  
  notepad %USERPROFILE%\RiskScape\secrets.ini

For more details on configuring secrets in RiskScape, refer to:
https://engine-docs.sites.riskscape.nz/reference/config/secrets.html

## Type information

All the StatsNZ bookmarks conform to the same RiskScape type (i.e. the `Region` type).
This means that the attributes will be consistently named regardless of which StatsNZ layer you
choose to use - you can swap one StatsNZ bookmark out for another without affecting the model.

## Licensing

The datasets in this directory are made available by StatsNZ, licensed under the Creative Commons 4.0 Creative Commons Attribution 4.0 International.
Refer to https://datafinder.stats.govt.nz/license/attribution-4-0-international
