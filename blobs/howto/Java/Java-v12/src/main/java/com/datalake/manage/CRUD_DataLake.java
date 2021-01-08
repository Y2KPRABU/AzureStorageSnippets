package com.datalake.manage;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedInputStream;
import java.io.OutputStream;
import java.security.InvalidKeyException;
import java.net.URISyntaxException;
import com.azure.core.http.rest.PagedIterable;
import com.azure.storage.file.datalake.DataLakeDirectoryClient;
import com.azure.storage.file.datalake.DataLakeFileClient;
import com.azure.storage.file.datalake.DataLakeFileSystemClient;
import com.azure.storage.file.datalake.DataLakeServiceClient;
import com.azure.storage.file.datalake.models.ListPathsOptions;
import com.azure.storage.file.datalake.models.PathItem;


public class CRUD_DataLake {
    
    // ----------------------------------------------------------
    // Create a file system
    // ----------------------------------------------------------
    
    public DataLakeFileSystemClient CreateFileSystem
    (DataLakeServiceClient serviceClient){

        return serviceClient.createFileSystem("my-file-system");
    }

    // ----------------------------------------------------------
    // Get a file system
    // ----------------------------------------------------------

    public DataLakeFileSystemClient GetFileSystem
    (DataLakeServiceClient serviceClient, String fileSystemName){
        
        DataLakeFileSystemClient fileSystemClient =
            serviceClient.getFileSystemClient(fileSystemName);

        return fileSystemClient;
    }

    // ----------------------------------------------------------
    // Create directory
    // ----------------------------------------------------------

    public DataLakeDirectoryClient CreateDirectory
    (DataLakeServiceClient serviceClient, String fileSystemName){
    
        DataLakeFileSystemClient fileSystemClient =
        serviceClient.getFileSystemClient(fileSystemName);

        DataLakeDirectoryClient directoryClient =
            fileSystemClient.createDirectory("my-directory");

        return directoryClient.createSubdirectory("my-subdirectory");
    }
    
    // ----------------------------------------------------------
    // Get a directory
    // ----------------------------------------------------------

    public DataLakeDirectoryClient GetDirectory
    (DataLakeFileSystemClient fileSystemClient, String directoryName){

        DataLakeDirectoryClient directoryClient =
            fileSystemClient.getDirectoryClient(directoryName);

        return directoryClient;
    }
    
    // ---------------------------------------------------------
    // Rename a directory
    //----------------------------------------------------------

    public DataLakeDirectoryClient
        RenameDirectory(DataLakeFileSystemClient fileSystemClient){

        DataLakeDirectoryClient directoryClient =
            fileSystemClient.getDirectoryClient("my-directory/my-subdirectory");

        return directoryClient.rename(fileSystemClient.getFileSystemName(),"my-subdirectory-renamed");
    }
  
    // ---------------------------------------------------------
    // Move a directory
    //----------------------------------------------------------

    public DataLakeDirectoryClient MoveDirectory
    (DataLakeFileSystemClient fileSystemClient){

        DataLakeDirectoryClient directoryClient =
            fileSystemClient.getDirectoryClient("my-directory/my-subdirectory-renamed");

        return directoryClient.rename(fileSystemClient.getFileSystemName(),"my-directory-2/my-subdirectory-renamed");                
    }
  
    // ----------------------------------------------------------
    // Delete directory
    // ----------------------------------------------------------

    public void DeleteDirectory(DataLakeFileSystemClient fileSystemClient){
        
        DataLakeDirectoryClient directoryClient =
            fileSystemClient.getDirectoryClient("my-directory");

        directoryClient.deleteWithResponse(true, null, null, null);
    }

    // ----------------------------------------------------------
    // List directory contents
    // ----------------------------------------------------------

    public void ListFilesInDirectory(DataLakeFileSystemClient fileSystemClient){
        
        ListPathsOptions options = new ListPathsOptions();
        options.setPath("my-directory");
     
        PagedIterable<PathItem> pagedIterable = 
        fileSystemClient.listPaths(options, null);

        java.util.Iterator<PathItem> iterator = pagedIterable.iterator();

       
        PathItem item = iterator.next();

        while (item != null)
        {
            System.out.println(item.getName());


            if (!iterator.hasNext())
            {
                break;
            }
            
            item = iterator.next();
        }

    }

    // ----------------------------------------------------------
    // Upload files to directory
    // ----------------------------------------------------------

    public void UploadFile(DataLakeFileSystemClient fileSystemClient) 
        throws FileNotFoundException{
        
        DataLakeDirectoryClient directoryClient =
            fileSystemClient.getDirectoryClient("my-directory");

        DataLakeFileClient fileClient = directoryClient.createFile("uploaded-file.txt");

        File file = new File("C:\\Users\\normesta\\Norms-Test-Projects\\mytestfile.txt");

     //   InputStream targetStream = new FileInputStream(file);
        InputStream targetStream = new BufferedInputStream(new FileInputStream(file));

        long fileSize = file.length();

        fileClient.append(targetStream, 0, fileSize);

        fileClient.flush(fileSize);
    }

    // ----------------------------------------------------------
    // Upload files in bulk
    // ----------------------------------------------------------

    public void UploadFileBulk(DataLakeFileSystemClient fileSystemClient) 
        throws FileNotFoundException{
        
        DataLakeDirectoryClient directoryClient =
            fileSystemClient.getDirectoryClient("my-directory");

        DataLakeFileClient fileClient = directoryClient.getFileClient("uploaded-file.txt");

        fileClient.uploadFromFile("C:\\Users\\normesta\\Norms-Test-Projects\\mytestfile.txt");

    }
   
    // ----------------------------------------------------------
    // Download a file from a directory (binary)
    // ----------------------------------------------------------
    public void DownloadFile(DataLakeFileSystemClient fileSystemClient)
      throws FileNotFoundException, java.io.IOException{

        DataLakeDirectoryClient directoryClient =
            fileSystemClient.getDirectoryClient("my-directory");

        DataLakeFileClient fileClient = 
            directoryClient.getFileClient("uploaded-file.txt");

        File file = new File("C:\\Users\\normesta\\Norms-Test-Projects\\downloadedFile.txt");

        OutputStream targetStream = new FileOutputStream(file);
        
        fileClient.read(targetStream);

        targetStream.close();

        fileClient.flush(file.length());
        
    }

    // ----------------------------------------------------------
    // Driver Menu
    // ----------------------------------------------------------

    public void ShowMenu() throws java.lang.Exception, URISyntaxException, InvalidKeyException{
        
        try {

            DataLakeServiceClient dataLakeServiceClient = Authorize_DataLake.GetDataLakeServiceClient
                (Constants.storageAccountName, Constants.accountKey);

            // Uncomment if you want to test AD Authorization.
            // DataLakeServiceClient dataLakeServiceClient = Authorize_DataLake.GetDataLakeServiceClient
            //    (accountName, clientID, clientSecret, tenantID);

            DataLakeFileSystemClient fileSystemClient = GetFileSystem(dataLakeServiceClient, Constants.containerName);

            // Listening for commands from the console
            System.out.print("\033[H\033[2J");  
            System.out.flush();

            System.out.println("Enter a command");

            System.out.println("(1) Add file system (2) Add directory | (3) Rename directory | " +
            "(4) Delete directory | (5) Upload a file to a directory | (6) Upload in bulk | " + 
            " (7) List files in directory | (8) Get files from directory | (9) Exit");

            BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));

            while (true) {

                System.out.println("# Enter a command : ");
                String input = reader.readLine();

                switch(input){

                    case "1":
                       fileSystemClient = CreateFileSystem(dataLakeServiceClient);
                    break;
                    case "2":
                        CreateDirectory(dataLakeServiceClient, Constants.containerName);
                    break;
                    case "3":
                        RenameDirectory(fileSystemClient);
                        break;
                    case "4":
                        DeleteDirectory(fileSystemClient);
                        break;
                    case "5":
                        UploadFile(fileSystemClient);
                    break;
                    case "6":
                        ListFilesInDirectory(fileSystemClient);
                    break;
                    case "7":
                        DownloadFile(fileSystemClient);
                    break;
                    case "8":
                       UploadFileBulk(fileSystemClient);
                    break;
                    case "9":
                    return;
                    default:
                        break;
                }
            }
        } catch (java.lang.Exception e) {
            System.out.println(e.toString());
            System.exit(-1);

        }

    }
}
