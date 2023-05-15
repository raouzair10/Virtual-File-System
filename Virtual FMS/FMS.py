import os
import sys

# You can change the block size and the number of blocks below (the ones mentioned below are just test values)
# NOTE: Empty the sample.txt file before you change the block size
max_size = 5
num_of_blocks = 10

# making an empty 2d list for memory (each sublist represents a block in memory)
memory = []
for i in range(num_of_blocks):
    memory.append([])

# a class for the file objects
class File:
    # initialising data members
    def __init__(self, fName):
        self.name = fName
        self.blocks = []
        self.size = 0
        self.mode = None
        self.parent = None
        self.path = []

    # a function to read content from the file
    def Read_from_file(*args):
        self = args[0]

        # read the entire file contents
        if len(args) == 1:
            str = ""
            for i in self.blocks:
                for j in memory[i]:
                    str += j
            return str
        
        # read file contents from the provided starting index upto the required number of characters
        if len(args) == 3:
                total_characters = 0
                file_contents = ""
                str = ""
                starting_index = args[1]
                for i in self.blocks:
                    for j in memory[i]:
                        file_contents += j
                while(total_characters != args[2]):
                    if args[1] + args[2] <= self.size:
                        str += file_contents[starting_index]
                        starting_index += 1
                        total_characters += 1
                    else:
                        str = file_contents[starting_index:-1]
                        break
                return str

    # a function to write data to the file
    def Write_to_file(*args):
        self = args[0]

        # reading the complete file in "content" variable and emptying its content from the memory
        content = self.Read_from_file()
        for block in self.blocks:
                memory[block].clear()
        self.blocks.clear()

        # (append mode) appending new text at the end of the "content" variable
        if len(args) == 2:
            text = args[1]
            content += text

        # (write_at mode) placing new text at the provided position of the "content" variable
        else:
            pos, text = args[1], args[2]
            l = len(content)
            for i in text:
                if pos < l:
                    content = content[:pos] + i + content[pos+1:]
                    pos += 1
                else:
                    content += i

        # finding an empty block as a starting block to write the string "content"
        for block in range(len(memory)):
            if len(memory[block]) == 0:
                break
        
        # writing the string "content" in the memory starting from the empty block found above
        k = 0
        written = False
        while written == False:

            # writing in the current empty block
            for ch in range(k, len(content)):
                if len(memory[block]) < max_size:
                    memory[block].append(content[ch])                        
                else:
                    k = ch
                    break
                if ch == len(content) - 1:
                    written = True
            self.blocks.append(block)

            # finding the next empty block
            for i in range(block + 1, len(memory)):
                    if len(memory[i]) == 0:
                        block = i
                        break
        
        # after rewriting to the memory, resetting the size of file
        self.size = 0
        for i in self.blocks:
            self.size += len(memory[i])

    # a function to move content within a file
    def Move_within_file(self, start, size, target):
        # reading the whole file into a string variable "file_content", which will be manipulated, and then rewritten in memory
        file_content = self.Read_from_file()
        content_to_move = file_content[start : start+size]

        # moving content behind its actual position
        if target < start:
            file_content = file_content[:start] + file_content[start+size:]
            file_content = file_content[:target] + content_to_move + file_content[target:]

        # moving content in front of its actual position
        else:
            file_content = file_content[:target] + content_to_move + file_content[target:]
            file_content = file_content[:start] + file_content[start+size:]

        # clearing the memory first, before rewriting
        for block in self.blocks:
                memory[block].clear()
        self.blocks.clear()

        # rewriting updated file content to the memory
        self.Write_to_file(file_content)


    # a function to truncate the file to the provided size
    def Truncate_file(self,size):
        # reading the complete file into a string variable "file_content"
        file_content = self.Read_from_file()

        # slicing the string upto the provided size
        if size < len(file_content):
            file_content = file_content[:size]
        
        # clearing the memory before rewriting
        for block in self.blocks:
                memory[block].clear()
        self.blocks.clear()

        # rewriting the truncated content to the memory
        self.Write_to_file(file_content)

# a class for directory objects
class Directory:
    # a list which will only store the home directory (the rest of the directories will be stored within the home directory)
    dirs = []

    # a class variable to store the current working directory object
    currentDir = None

    # initialising data members
    def __init__(self, dirName):
        self.name = dirName
        self.items = []
        self.num_of_files = 0
        self.num_of_dirs = 0
        self.parent = None
        self.path = []

# a function to create a new directory
def mkDir(dirName):
    tempCurrentDir = Directory.currentDir
    hierarchy = dirName.split("/")
    dirName = hierarchy.pop()

    # finding the parent directory
    for dname in hierarchy:
        found = False
        if dname == "home":
            tempCurrentDir = Directory.dirs[0]
            continue
        for dir in tempCurrentDir.items:
            if isinstance(dir, Directory) and dir.name == dname:
                tempCurrentDir = dir
                found = True
                break
        if not found:
            print("Invalid path given!")
            return
        
    # checking if a directory with same name already exists
    for i in tempCurrentDir.items:
        if isinstance(i, Directory) and i.name == dirName:
            print(f"\nDirectory {dirName} already exists!")
            return False
        
    # creating the directory inside the parent directory
    tempCurrentDir.items.insert(0, Directory(dirName))
    tempCurrentDir.num_of_dirs += 1
    
    # setting the parent and path of the new directory
    d = tempCurrentDir.items[0]
    d.parent = tempCurrentDir
    while d.parent != None:
        tempCurrentDir.items[0].path.insert(0, d.parent.name)
        d = d.parent
    tempCurrentDir.items[0].path.append(dirName)
    return True

# a function to change the current working directory
def chDir(dirName):
    hierarchy = dirName.split("/")

    # finding the directory
    for dname in hierarchy:
        found = False
        if dname == "home":
            Directory.currentDir = Directory.dirs[0]
            continue
        for dir in Directory.currentDir.items:
            if isinstance(dir, Directory) and dir.name == dname:

                # setting the given directory as the current directory
                Directory.currentDir = dir
                found = True
                break
        if not found:
            print("\nNo such directory exists!")
            return
    print("\nCurrent working directory: " + dirName)

# a function to move a file from one directory to another
def move(source, dest):
    source_hierarchy = source.split("/")
    fName = source_hierarchy.pop()
    dest_hierarchy = dest.split("/")
    tempSourceDir = Directory.currentDir

    # finding the source directory
    for dname in source_hierarchy:
        found1, found2 = False, False
        if dname == "home":
            tempSourceDir = Directory.dirs[0]
            continue
        for dir in tempSourceDir.items:
            if isinstance(dir, Directory) and dir.name == dname:
                tempSourceDir = dir
                found1 = True
                break

    # finding the file in the source directory
    for f in tempSourceDir.items:
        if isinstance(f, File) and f.name == fName:
            found2 = True
            break
    if not found1 or not found2:
        print("\nNo such file or directory!")

    # finding the destination directory
    for dname in dest_hierarchy:
        found3 = False
        if dname == "home":
            tempDestDir = Directory.dirs[0]
            continue
        for dir in tempDestDir.items:
            if isinstance(dir, Directory) and dir.name == dname:
                tempDestDir = dir
                found3 = True
                break
        if not found3:
            print("\nInvalid destination path!")

    # adding the file to the destination directory
    tempDestDir.items.append(f)
    tempDestDir.num_of_files += 1
    d = tempDestDir.items[-1]

    # resetting file path
    d.parent = tempDestDir
    f.path.clear()
    while d.parent != None:
        f.path.insert(0, d.parent.name)
        d = d.parent
    f.path.append(f.name)

    # deleting file from source directory
    for i, f in enumerate(tempSourceDir.items):
        if isinstance(f, File) and f.name == fName:
            del tempSourceDir.items[i]
            tempSourceDir.num_of_files -= 1

# a function to create a new file
def create(fName):
    tempCurrentDir = Directory.currentDir
    hierarchy = fName.split("/")
    fName = hierarchy.pop()

    # finding the parent directory where we want to create the file
    for dname in hierarchy:
        found = False
        if dname == "home":
            tempCurrentDir = Directory.dirs[0]
            continue
        for dir in tempCurrentDir.items:
            if isinstance(dir, Directory) and dir.name == dname:
                tempCurrentDir = dir
                found = True
                break
        if not found:
            print("\nInvalid path given!")
            return False
        
    # checking if a file with same name already exists
    for i in tempCurrentDir.items:
        if isinstance(i, File) and i.name == fName:
            print(f"\nFile {fName} already exists!")
            return False
        
    # creating the file inside the parent directory
    tempCurrentDir.items.append(File(fName))

    # setting the parent and path of the file
    d = tempCurrentDir.items[-1]
    d.parent = tempCurrentDir
    while d.parent != None:
        tempCurrentDir.items[-1].path.insert(0, d.parent.name)
        d = d.parent
    tempCurrentDir.items[-1].path.append(fName)
    tempCurrentDir.num_of_files += 1
    return True

# a function to open the file (it returns the file object if file is found)
def openFile(fName, mode):
    tempCurrentDir = Directory.currentDir
    hierarchy = fName.split("/")
    fName = hierarchy.pop()

    # finding the parent directory
    for dname in hierarchy:
        found = False
        if dname == "home":
            tempCurrentDir = Directory.dirs[0]
            continue
        for dir in tempCurrentDir.items:
            if isinstance(dir, Directory) and dir.name == dname:
                tempCurrentDir = dir
                found = True
                break
        if not found:
            return None
        
    # finding the file inside the parent directory
    for f in tempCurrentDir.items:
        if isinstance(f, File) and f.name == fName:

            # setting the file's mode and returning the file object
            f.mode = mode
            return f

# a function to close the file (it resets its mode to "None")
def closeFile(fName):
    tempCurrentDir = Directory.currentDir
    hierarchy = fName.split("/")
    fName = hierarchy.pop()

    # finding the parent directory
    for dname in hierarchy:
        found = False
        if dname == "home":
            tempCurrentDir = Directory.dirs[0]
            continue
        for dir in tempCurrentDir.items:
            if isinstance(dir, Directory) and dir.name == dname:
                tempCurrentDir = dir
                found = True
                break
        if not found:
            print("\nNo such file or directory!")
            return
    
    # finding the file in parent directory
    for f in tempCurrentDir.items:
        if isinstance(f, File) and f.name == fName:

            # closing the file
            print("\nFile " + f.name + " closed!")
            f.mode = None

# a function to delete the file
def delete(fName):
    tempCurrentDir = Directory.currentDir
    hierarchy = fName.split("/")
    fName = hierarchy.pop()

    # finding the parent directory
    for dname in hierarchy:
        found = False
        if dname == "home":
            tempCurrentDir = Directory.dirs[0]
            continue
        for dir in tempCurrentDir.items:
            if isinstance(dir, Directory) and dir.name == dname:
                tempCurrentDir = dir
                found = True
                break
        if not found:
            print("\nNo such file or directory!")
            return
    
    # finding the file to delete in the parent directory
    for i, f in enumerate(tempCurrentDir.items):
        if isinstance(f, File) and f.name == fName:

            # clearing up the file's content from the memory
            for block in f.blocks:
                memory[block].clear()

            # deleting the file object
            del tempCurrentDir.items[i]
            tempCurrentDir.num_of_files -= 1
            print("\nFile " + f.name + " deleted!")
            return

# a function to show the memory map (it uses a recursive call to move to directories within directories)
def showMemoryMap(tempCurrentDir):

    # getting directory path
    dpath = "/".join(tempCurrentDir.path)
    print()

    # printing the details of the directory for which this function is called recursively
    print("\t"*(len(tempCurrentDir.path)-1), end="")
    print(f"D-Name = {tempCurrentDir.name}\tNum-Dirs = {tempCurrentDir.num_of_dirs}\tNum-Files = {tempCurrentDir.num_of_files}\tComplete Path = {dpath}")
    
    # printing the details of all the files of the directory for which this function is called recursively
    for f in tempCurrentDir.items:
        if isinstance(f, File):
            fpath = "/".join(f.path)
            print()
            print("\t"*(len(f.path)-1), end="")
            print(f"File Name = {f.name}\tSize = {f.size}\tBlocks Used = {f.blocks}\tComplete Path = {fpath}")
    
    # a recursive call for its subdirectories
    for i in range(tempCurrentDir.num_of_dirs):
        showMemoryMap(tempCurrentDir.items[i])

# a utility function which populates a list passed to it with information of all the directories and files
def hierarchy(tempCurrentDir, l):
    dpath = "/".join(tempCurrentDir.path)
    l.append(dpath)
    for f in tempCurrentDir.items:
        if isinstance(f, File):
            fpath = "/".join(f.path)
            b = f.blocks[:]
            for i in range(len(b)):
                b[i] = str(b[i])
            bl = ",".join(b)
            if len(bl) == 0:
                fpath = fpath + " " + str(f.size) + " -1" 
            else:
                fpath = fpath + " " + str(f.size) + " " + bl
            l.append(fpath)
    for i in range(tempCurrentDir.num_of_dirs):
        hierarchy(tempCurrentDir.items[i], l)

# a function to save the state of the system before we terminate the program
def saveState():
    l = []
    hierarchy(Directory.dirs[0], l)
    del l[0]
    with open(os.path.join(sys.path[0], "sample.txt"), "w") as f:
        for i in l:
            f.write(i + "\n")
        f.write("\n")
        for i in memory:
            str = ""
            for j in i:
                str += j
            while len(str) < max_size:
                str += "_"
            f.write(str + "\n") 

# a function to load the state of the system when we start the program
def loadState():
    with open(os.path.join(sys.path[0], "sample.txt"), "r") as f:
        m = False
        count = 0
        for x in f:
            l = x.split()
            if x.strip() == "":
                m = True
                continue
            elif len(l) == 1 and not m:
                mkDir(l[0])
            elif len(l) == 3:
                create(l[0])
                a = openFile(l[0], "rw")
                a.size = int(l[1])
                b = l[2].split(",")
                for c in b:
                    if c != "-1":
                        a.blocks.append(int(c))
            else:
                for i in range(max_size):
                    if x[i] != "_":
                        memory[count].append(x[i])
                count += 1

# main function
def main():
    print("\n----------------------VIRTUAL FILE MANAGEMENT SYSTEM----------------------\n")
    print("NOTE: When asked for file name or directory name, either just enter the name or enter complete path.")
    print("--> If you just enter the name, the current working directory will be manipulated.")
    print("--> If you give complete path, the directory mentioned in that path will be manipulated.\n")
    if len(Directory.dirs) == 0:
        Directory.dirs.append(Directory("home"))
        Directory.dirs[0].path.append("home")
    chDir("home")
    loadState()
    flag = True
    file = None
    while flag:
        print("\nChoose what you want to do from the given options.")
        print("1. Create Directory")
        print("2. Change Directory")
        print("3. Create File")
        print("4. Open File")
        print("5. Close File")
        print("6. Delete File")
        print("7. Read from File")
        print("8. Write to File")
        print("9. Move within File")
        print("10. Truncate File")
        print("11. Show Memory Map")
        print("12. Exit")
        
        choice = input("\nEnter your choice (1-12): ")
        
        if choice == "1":
            dirName = input("\nEnter directory name: ")
            dcreated = mkDir(dirName)
            if dcreated:
                print("\nDirectory created!")
        
        elif choice == "2":
            dirName = input("\nEnter directory name: ")
            chDir(dirName)
        
        elif choice == "3":
            fName = input("\nEnter file name: ")
            fcreated = create(fName)
            if fcreated:
                print("\nFile created!")
        
        elif choice == "4":
            fName = input("\nEnter file name: ")
            mode = input("Choose mode (r/w/rw): ")
            file = openFile(fName, mode)
            if file:
                print("\nFile opened in " + file.mode + " mode.")
            else:
                print("\nNo such file or directory!")
        
        elif choice == "5":
            fName = input("\nEnter file name: ")
            closeFile(fName)
        
        elif choice == "6":
            fName = input("\nEnter file name: ")
            delete(fName)
        
        elif choice == "7":
            if file:
                if file.mode == "r" or file.mode == "rw":
                    read_type = input("\nWould you like to 1. read the entire file OR 2. read from a specific index? (1/2):")
                    if read_type == "1":
                        print("\nFile contents:")
                        print(file.Read_from_file())
                    elif read_type == "2":
                        start = int(input("\nEnter the starting index: "))
                        size = int(input("Enter the number of characters you want to read: "))
                        print("\nFile content: ")
                        print(file.Read_from_file(start,size))
                    else:
                        print("\nInvalid choice.")
                else:
                    print("\nFile not in read mode.")
            else:
                print("\nFirst open the file (in read mode) you want to read!")
        elif choice == "8":
            if file:
                if file.mode == "rw" or file.mode == "w":
                    write_type = input("\nWould you like to: 1. append text to the file OR 2. write at some specific index? (1/2): ")
                    if write_type == "1":
                        text = input("\nEnter the text: ")
                        file.Write_to_file(text)
                        print("\nText written to file!")
                    elif write_type == "2":
                        start = int(input("\nEnter the index where you want to write at: "))
                        text = input("\nEnter the text (this may overwrite text at that index): ")
                        file.Write_to_file(start,text)
                        print("\nText written to file!")
                    else:
                        print("\nInvalid choice!")
                else:
                    print("\nFile not in write mode!")
            else:
                print("\nFirst open the file (in write mode) in which you want to write!")

        elif choice == "9":
            if file:
                start = int(input("\nEnter starting index: "))
                size = int(input("Enter the number of characters to move: "))
                target = int(input("Enter target index: "))
                file.Move_within_file(start, size, target)
                print("\nContent moved within file!")
            else:
                print("\nFirst open the file (in write mode) in which you want to move content!")
        
        elif choice == "10":
            if file:
                size = int(input("\nEnter new size (this will reset the size of the file, the rest of the data will be deleted): "))
                file.Truncate_file(size)
                print("\nFile truncated!")
            else:
                print("\nFirst open the file (in write mode) which you want to truncate!")
        
        elif choice == "11":
            print("\n--------------------------MEMORY MAP--------------------------")
            showMemoryMap(Directory.dirs[0])

        elif choice == "12":
            saveState()
            print("\nThank you for using our virtual file management system!")
            flag = False

        else:
            print("Invalid Choice!")
        
        print("\n--------------------------------------------------------")

# calling the main function
main()
