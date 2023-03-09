package com.blobs.queryendpoint;

import com.azure.identity.*;
import com.azure.resourcemanager.*;
import com.azure.resourcemanager.storage.models.*;
import com.azure.core.management.*;
import com.azure.core.management.profile.*;

public class AccountProperties {
    // <Snippet_QueryEndpoint>
    public String GetBlobServiceEndpoint(String saName, DefaultAzureCredential credential) {
        String subscriptionID = "<subscription-id>";
        String rgName = "<resource-group-name>";
        AzureProfile profile = new AzureProfile(AzureEnvironment.AZURE);

        AzureResourceManager azureResourceManager = AzureResourceManager
                .configure()
                .authenticate(credential, profile)
                .withSubscription(subscriptionID);

        StorageAccount storageAccount = azureResourceManager.storageAccounts()
                .getByResourceGroup(rgName, saName);

        String endpoint = storageAccount.endPoints().primary().blob();

        return endpoint;
    }
    // </Snippet_QueryEndpoint>
}
