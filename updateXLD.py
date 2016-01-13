import os.path
import time
import shutil
import os
import fileinput
import string
import pprint

#stop XLD or XLR Service
#os.system("service stop xldeploy")
#pause for service to stop
#time.sleep(25)

print "XL Deploy service is shutting down for upgrade!"
# list the persistent directories from XLD that need to be copied
directories = ['ext', 'conf', 'plugins', 'repository', 'work', 'bin']

#print os.path.dirname(os.path.realpath(__file__))
xld_install = os.path.dirname(os.path.realpath(__file__))

# location to save move repository, ext, plugins and conf directores

save_path = "/" + raw_input("Please input the new shared path for your XL Deploy repository: ") #this can be changed to a hardcoded location such as /opt/xebialabs/XLDeploy

#location of XLD install
#xld_install = raw_input("Please enter the location of your XL Deploy Server: ")

#create folders to organize reposititory if they don't exist
if not os.path.exists(save_path):
    #print save_path, "Creating shared repository path for: ", new_folder
    os.makedirs(save_path)
    print "Creating directory: ", save_path

    #compile location for new repository
    for dir in directories:
        new_folder = str(save_path) + "/" + str(dir)
        old_loc = os.path.dirname(os.path.realpath(__file__)) + "/" + dir #XLD/XLR Core Directory can be hardcoded here
        print old_loc
        print "New Folder: ", new_folder
        print "Directory: ", dir

        #copy repository from install of XLD/XLR to specified save_path
        try:
            shutil.copytree(dir, new_folder)
        # Directories are the same
        except shutil.Error as e:
            print('Directory not copied. Error: %s' % e)
        # Any error saying that the directory doesn't exist
        except OSError as e:
            print('Directory not copied. Error: %s' % e)
        
        #remove the folders from the new install
        shutil.rmtree(old_loc)
        print "Removing ", old_loc
        
        #symlink the shared folders
        os.system("ln -s " + new_folder + " " + old_loc)
        #print "ln -s " + new_folder + " ", old_loc
        print "Symlinking ", new_folder + " to " + old_loc
        
        properties_file = save_path + "/conf/deployit.conf"
        repository_loc = "jcr.repository.path=file:/" + save_path + "/repository"
        oldProp ='jcr.repository.path=repository'
        
        print 'Updating the repository location in your ' + properties_file + " file from " + oldProp + " to " + repository_loc + "!"
        
        s = open(properties_file).read()
        s = s.replace(oldProp, repository_loc)
        f = open(properties_file, 'w')
        f.write(s)
        f.close()

else:
    print 'Your shared repository at ' + save_path + ' already exists I am Updating your XL Deploy server!'
    for dir in directories:
        new_folder = str(save_path) + "/" + str(dir)
        old_loc = os.path.dirname(os.path.realpath(__file__)) + "/" + dir #XLD/XLR Core Directory can be hardcoded here
        #remove the folders from the new install
        shutil.rmtree(old_loc)
        print "Removing ", old_loc

        #symlink the shared folders
        os.system("ln -s " + new_folder + " " + old_loc)
        #print "ln -s " + new_folder + " ", old_loc
        print "Symlinking ", new_folder + " to " + old_loc