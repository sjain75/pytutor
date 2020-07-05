# Pytutor

Pytutor is a ...

## Setup and testing

0. Download release

1. Get in touch with us to be assigned an IAM user and for us to create appropriate directories for hosting you
        
        (obs. if awscli setup use prebuilt script to create a folder in the bucket to host their static worksheet pages
        Obs. Use their IAM user account to manually create it ) 

        (*) Test if pytutor.ddns.net/[user]/pages/pytutor-demo.html

2. Add your aws credentials to access your bucket

3. Create a worksheet using the Worksheet Creator

4. Upload answers.json and html file to the s3
    -> Manually drag and drop upload files to s3 <b>OR</b>      
    -> Use provided sync-s3.py script 

5. pytutor.ddns.net/[user]/worksheets/html/[WSCODE].html

## Worksheet Creator Usage

## Attempting worksheets

## Appendix

<b>* Bucket Structure </b>

pytutor.ddns.net 
        * userDirectory //tyler, meena, ... //everything inside only accessible by user  
                * worksheets  
                        * report  
                        * html //public  
                        * answers  
                        * masterReport.json  
                * student  
                        * username.json  
                * pages  
                        * Sample Pages //allows users to create a home page //home.html //public  
                        * Page to access student report from  //Template, makes users login from front-end using GAPI and then loads data through ajax request to lamdba  
        * js   
        * styles   
        * user-permission for requests directed in through lambda //for example request for report from front end to lambda //super-private  

<b>* Github repo Sturcutre on User computers</b>  
        * WorksheetCreator  
                * creator.py file  
                * test Py files  
        * pages  
                * home.html //can be pushed up to s3 bucket  
        * worksheets //can be pushed up to s3 bucket  
                * html  
                * answers  
        * js  
        * styles  
        * ionic  
        * resources  
        
## Glossary

*Our users are Professors

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

