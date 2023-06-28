import PyPDF2
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

config = {
    'merged_filename': '_merged.pdf',
    'directory_to_watch': '//uhmc-fs-share/Shares/RadOnc/Planning/_merge_pdf'
}

marged_filename =  config['merged_filename']
directory_path = config['directory_to_watch']

print('watching directory: ', directory_path)

def list_pdf_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    pdf_files = sorted([file for file in files if file.endswith('.pdf') and not file.startswith('_')])
    pdf_paths = [os.path.join(folder_path, file) for file in pdf_files]
    return pdf_paths

def merge_pdfs(output_file, pdfs):
    merger = PyPDF2.PdfWriter()
    
    for pdf in pdfs:
        merger.append(pdf)
    
    merger.write(output_file)
    merger.close()

class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):

        filename = os.path.basename(event.src_path)
        print('filename-', filename)
        print(f"Event type: {event.event_type}  Path: {event.src_path}")

        if filename == marged_filename:
            print('merged file event - skip.')
        else:
            folder_path = os.path.dirname(event.src_path)
            output_file = os.path.join(folder_path, marged_filename)
            pdfs = list_pdf_files_in_folder(folder_path)
            if len(pdfs) > 0:
                merge_pdfs(output_file, pdfs)
                print('merging done - ' , output_file )
            else:
                print('no pdf files to merge!')


def run():
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, directory_path, recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    print('done.')
