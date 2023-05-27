# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

class BaseConfig(object):

    # Can be set to 'MasterUser' or 'ServicePrincipal'
    AUTHENTICATION_MODE = 'ServicePrincipal'

    # Workspace Id in which the report is present
    WORKSPACE_ID = 'ef0d41ba-8607-44b1-9d70-befa2898e90b'
    
    # Report Id for which Embed token needs to be generated
    # REPORT_ID = '8dfe7cb6-b6f2-4f19-a1d1-1fbc8f63ea98'
    REPORT_ID = '038608d1-55fa-402a-92ae-a3be92e3b749'#'ce9a62ce-9c85-4896-b514-bb252dde79f9'
    # Id of the Azure tenant in which AAD app and Power BI report is hosted. Required only for ServicePrincipal authentication mode.
    TENANT_ID = '98dbcdf5-72d2-4fdd-84c9-ae6ccee2916b'
    
    # Client Id (Application Id) of the AAD app
    CLIENT_ID = '860653e2-03cb-466a-8498-3b76b21434af'
    
    # Client Secret (App Secret) of the AAD app. Required only for ServicePrincipal authentication mode.
    CLIENT_SECRET = 'pGY8Q~rri-1PTBnDjY5JRZV~WofEa9ZouGKyzcO.'
    
    # Scope Base of AAD app. Use the below configuration to use all the permissions provided in the AAD app through Azure portal.
    SCOPE_BASE = ['https://analysis.windows.net/powerbi/api/.default']
    
    # URL used for initiating authorization request
    AUTHORITY_URL = 'https://login.microsoftonline.com/organizations'
    
    # Master user email address. Required only for MasterUser authentication mode.
    POWER_BI_USER = 'admin@M365x81071076.onmicrosoft.com'
    
    # Master user email password. Required only for MasterUser authentication mode.
    POWER_BI_PASS = 'eujOw1iuCT'