#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install asf_search


# In[11]:


import asf_search as asf


# In[12]:


session = asf.ASFSession()


# In[14]:


import getpass
username = input('Username:')
password = getpass.getpass('Password:')

try:
    user_pass_session = asf.ASFSession().auth_with_creds(username, password)
except asf.ASFAuthenticationError as e:
    print(f'Auth Failed: {e}')
else:
    print('Success!')


# In[19]:


aoi= 'POLYGON((-86.94296 40.45698,-86.93968 40.45692,-86.93972 40.45926, -86.93861 40.45910, -86.93746 40.45895, -86.93672 40.45879,-86.93562 40.45898,-86.93521 40.45929, -86.93484 40.45892,-86.93406 40.45748,-86.93430 40.45698, -86.93369 40.45595,-86.93197 40.45614,-86.93180 40.45508,-86.93291 40.45517,-86.93279 40.45336,-86.93168 40.45339,-86.93184 40.45171,-86.93139 40.45174,-86.93102 40.45021,-86.93078 40.44862,-86.93012 40.44628,-86.93201 40.44618,-86.93554 40.44615,-86.93558 40.44715,-86.93554 40.44868,-86.93677 40.44899,-86.93677 40.44974,-86.93722 40.45037,-86.93746 40.45105,-86.93763 40.45127,-86.93824 40.45158,-86.93890 40.45155,-86.93882 40.45090,-86.94300 40.45077,-86.94296 40.45698))'

opts = {
    'platform': asf.PLATFORM.ALOS,
    'instrument':asf.INSTRUMENT.PALSAR,
    'processingLevel':asf.PRODUCT_TYPE.RTC_HIGH_RES,
    'start': '2009-01-01T00:00:00Z',
    'end': '2011-02-01T23:59:59Z'
}


# In[21]:


results = asf.geo_search(intersectsWith=aoi, **opts)

print(f'{len(results)} results found')


# In[25]:


from os import listdir
results[0].download(path = r'C:\Users\Claudia Becerra\OneDrive - Universidad Nacional de Colombia\Documentos\GIS Project', session = user_pass_session)
listdir(r'C:\Users\Claudia Becerra\OneDrive - Universidad Nacional de Colombia\Documentos\GIS Project')

