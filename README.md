# zen
an python start project for demostrating unittest, logging, and package


#unit testing:  
python -m unittest discover -v
or
python -m unittest net.wyun.tests.prep.test_batch.TestBatch.test_al

logging configuration file:  
logging.conf

#Pycharm unittest configure
1. setup testing framework to be unittest
2. in 'edit configuration...' menu, select root of the project
    as the working directory

#references:  
http://plumberjack.blogspot.com/  
http://www.patricksoftwareblog.com/python-unit-testing-structuring-your-project/

#this project is the preprocess step for training the im2markup model
1. select all valid inkml files with latex truth
2. for all valid inkml files, separate them into 3 groups:
   a. train, b. validate, c. test
3. see test_batch.py for more info.
 
# useage:
1. copy all your inkml(with latex truth, the file would be discarded if no latex groundtruth)
   to data/batch/inkml folder.
2. copy all your xlsx file to data/xlsx/ folder
3. at the root of the project, run process.sh
4. it would generate im2markup training data: images in a folder + 4 lst files as shown in this screen 
shot. They are located in data/batch/ folder.
5. compress data/batch/ folder to batch.tar.gz
6. scp batch.tar.gz to training server, such as cuda2.
7. on training server, make a soft link:
xy00@cuda2:~/im2latex_tf$ ll formula_imageslrwxrwxrwx 1 xy00 xy00 32 Nov 10 00:19 formula_images -> /home/xy00/batch/formula_images//
8.  cp these 4 lst file to xy00@cuda2:~/im2latex_tf
9. remove old model files
10. run bash file: ./bash_train.sh in xy00@cuda2:~/im2latex_tf/

