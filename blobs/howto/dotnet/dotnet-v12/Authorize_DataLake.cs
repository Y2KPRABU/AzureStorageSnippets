using Azure;
using Azure.Core;
using Azure.Identity;
using Azure.Storage;
using Azure.Storage.Files.DataLake;
using Microsoft.Extensions.Azure;
using System;
using System.Collections.Generic;
using System.Text;

namespace dotnet_v12
{
    public static class Authorize_DataLake
    {
        //-------------------------------------------------------------
        // Connect to the storage account - get Data Lake service client
        //----------------------------------------------------------

        // <Snippet_AuthorizeWithKey>
        public static DataLakeServiceClient GetDataLakeServiceClient(string accountName, string accountKey)
        {
            StorageSharedKeyCredential sharedKeyCredential =
                new StorageSharedKeyCredential(accountName, accountKey);

           // string dfsUri = $"https://{accountName}.dfs.core.windows.net";
           string dfsUri = $"https://{accountName}.dfs.fabric.microsoft.com";

            DataLakeServiceClient dataLakeServiceClient = new DataLakeServiceClient(
                new Uri(dfsUri),
                sharedKeyCredential);

            return dataLakeServiceClient;
        }
        // </Snippet_AuthorizeWithKey>

        // ---------------------------------------------------------
        // Connect to the storage account (Azure AD - get Data Lake service client)
        //----------------------------------------------------------
        static InteractiveBrowserCredential tokenCredential = null;

        // <Snippet_AuthorizeWithAAD>
        public static DataLakeServiceClient GetDataLakeServiceClient(string accountName)
        {
          //  string dfsUri = $"https://{accountName}.dfs.core.windows.net";
           string dfsUri = $"https://{accountName}.dfs.fabric.microsoft.com";
            InteractiveBrowserCredentialOptions ibco = new InteractiveBrowserCredentialOptions
            {
                TokenCachePersistenceOptions = new TokenCachePersistenceOptions { Name = "tokcachefabric", UnsafeAllowUnencryptedStorage = true }
            };

            tokenCredential ??= new InteractiveBrowserCredential(ibco);
        DataLakeServiceClient dataLakeServiceClient = new(
                new Uri(dfsUri),
                tokenCredential);
            
            return dataLakeServiceClient;
        }
        // </Snippet_AuthorizeWithAAD>

        // <Snippet_AuthorizeWithSAS>
        public static DataLakeServiceClient GetDataLakeServiceClientSAS(string accountName, string sasToken)
        {
            //string dfsUri = $"https://{accountName}.dfs.core.windows.net";
           string dfsUri = $"https://{accountName}.dfs.fabric.microsoft.com";

            DataLakeServiceClient dataLakeServiceClient = new DataLakeServiceClient(
                new Uri(dfsUri),
                new AzureSasCredential(sasToken));

            return dataLakeServiceClient;
        }
        // </Snippet_AuthorizeWithSAS>
    }
}
