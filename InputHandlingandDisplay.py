import os

def StoretheUpoldedFile(Filename):
  # This funciton is defined to store the file uploded by the user into temporary file.
  # This is required as some librarys and functions requies to pass the file location instead of its contents, 
  # However,  file_uploader reads the file as a file-like Byte IO type : more can be found on 
  # https://blog.jcharistech.com/2021/01/21/how-to-save-uploaded-files-to-directory-in-streamlit-apps/
  # As I prefer to work on Streamlit share, I have no prioir informaion about the file location, 
  # so I use os.getcwd() to get the working directory and then add the uploaded file into it. 
  # we then use open-write to crate the file, more on https://www.w3schools.com/python/python_file_write.asp
  # finally we return the file locaion so that it can be used by other funciton 
  with open(os.path.join(os.getcwd(),Filename.name),"wb") as f:
      f.write(Filename.getbuffer())
  return (os.path.join(os.getcwd(),Filename.name))


