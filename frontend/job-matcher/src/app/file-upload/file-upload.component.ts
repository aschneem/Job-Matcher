import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-file-upload',
  standalone: true,
  imports: [],
  templateUrl: './file-upload.component.html',
  styleUrl: './file-upload.component.scss'
})
export class FileUploadComponent {
  @Output() fileUploaded = new EventEmitter<FileList>();

  onDragOver(event: DragEvent) {
    event.preventDefault(); // Prevent default browser behavior
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    if (event && event.dataTransfer && event.dataTransfer.files && event.dataTransfer.files.length > 0){
      this.fileUploaded.emit(event.dataTransfer.files);
    }
  }

  onFileChange(event: Event) {
    if (!event || !event.target){
      return;
    }
    const target = event.target as HTMLInputElement;
    const files = target.files;
    if (files && files.length > 0) {
      this.fileUploaded.emit(files);
    }
  }
}
