import os

def get_files_of_type(rootdir, extension):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(originalFolder):
        files = (f for f in filenames if f[(-1*len(extension)):] == extension)
        f.extend(files)
        subfiles = (get_files_of_type(os.path.join(dirpath, d), extension) for d in dirnames)
        f.extend(subfiles)
    
    return f


location  = "C:/Users/fdaly/Videos"

originalFolder = ("%s/Peppa Orig" % location)

outputFolder = ("%s/Peppa Converted" % location)

ffmpeg = "C:/Program Files (x86)/ffmpeg/bin/ffmpeg.exe"

aviFiles = get_files_of_type(originalFolder, "avi")

print(aviFiles)

for filename in aviFiles :
    
    folderName = os.path.basename(os.path.dirname(filename))

    outputSubFolder = os.path.join(outputFolder, foldername) 

    if(not os.path.exists(outputSubFolder)): 
        os.mkdir(outputSubFolder)
    

    outputFile = ("%s/%smp4" % (outputSubFolder, filename[:len(filename)-3]))
    

    if(os.path.exists(outputFile)):
       print ("File '%s' already exists. Skipping." % outputFile)
    else:
        print ("Converting '%s'" % filename)
       # Start-Process -FilePath $ffmpeg -ArgumentList ("-i ""{0}"" ""{1}""" -f $file.FullName, $outputFile) -Wait -NoNewWindow
    


