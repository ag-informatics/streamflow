#!/usr/bin/env python
# coding: utf-8

# In[45]:


import geopandas
import numpy as np
import asf_search as asf


# In[46]:


import sys ; sys.prefix


# In[47]:


import sys
sys.path.append("C:\OSGeo4W\apps\Python39\Lib")


# In[6]:


import os


# In[9]:


import sys
sys.path.append("C:\OSGeo4W\apps\qgis\python\qgis")


# In[34]:


points = geopandas.read_file(r'C:\Users\Claudia Becerra\OneDrive - Universidad Nacional de Colombia\Documentos\GIS Project\puntos.shp')
points


# In[48]:


polygon = geopandas.read_file(r'C:\Users\Claudia Becerra\OneDrive - Universidad Nacional de Colombia\Documentos\GIS Project\Farm.shp')
polygon


# In[52]:


coordinates = polygon['geometry'].to_wkt()
aoi = coordinates[0]
aoi


# In[17]:


session = asf.ASFSession()


# In[53]:


import getpass
username = input('Username:')
password = getpass.getpass('Password:')

try:
    user_pass_session = asf.ASFSession().auth_with_creds(username, password)
except asf.ASFAuthenticationError as e:
    print(f'Auth Failed: {e}')
else:
    print('Success!')


# In[54]:


opts = {
    'platform': asf.PLATFORM.ALOS,
    'instrument':asf.INSTRUMENT.PALSAR,
    'processingLevel':asf.PRODUCT_TYPE.RTC_HIGH_RES,
    'start': '2009-01-01T00:00:00Z',
    'end': '2011-02-01T23:59:59Z'
}


# In[55]:


results = asf.geo_search(intersectsWith=aoi, **opts)

print(f'{len(results)} results found')


# In[ ]:




