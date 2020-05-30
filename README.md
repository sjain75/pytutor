# PYTUTOR

**pages/** : The front end pages. Normally only contains .html files.

**styles/** : Styling for the front end pages. Normally only contains .css files.

**js/** : Add interactivity to the front end pages. Ties the front end to the backend. Normally only contains .js files.

**resources/** : Continas any resources to load on the front end. Example files: .svg, .jpgs, .pngs, etc.

**backend/** : Files on the server side. Talks to the databases. <br/>
               * Note: Currently includes [lambda_function](backend/lambda_function.py) which talks to the [s3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html) (concerns only AWS).
ii
