import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { FileService } from '../file.service';
import { Router, ActivatedRoute } from '@angular/router';
import { ChangeDetectorRef } from '@angular/core';
import { AlertService } from '../alert.service';

@Component({
  selector: 'app-red-plag',
  templateUrl: './red-plag.component.html',
  styleUrls: ['./red-plag.component.scss']
})
export class RedPlagComponent implements OnInit {
  blob: Blob;
  progress = 0;
  selectedFiles: FileList;
  currentFile: File;
  message;
	formGroup = this.fb.group({
    file: [null, Validators.required],
  });

  constructor(private fb: FormBuilder, private fileService: FileService, private router: Router, private alertService: AlertService, private cd: ChangeDetectorRef) { }

  ngOnInit(): void {
  	console.log("Fuck angular");
  }
  onFileChange(event) {
  console.log("file changed");
  let reader = new FileReader();
 
  if(event.target.files && event.target.files.length) {
    const [file] = event.target.files;
    reader.readAsDataURL(file);
  
    reader.onload = () => {
      this.formGroup.patchValue({
        file: reader.result
      });
      
      this.cd.markForCheck();
    };
  }
	}
	onSubmit() { 
  console.log("file upload ts");
  console.log(this.formGroup.value.file);
  this.fileService.postFile(this.formGroup.value).subscribe(
    event => {
      console.log(event);
    },
    err => {
      this.progress = 0;
      this.message = 'Could not upload the file!';
    });
	}
  onDownloadButtonClick() {
    console.log("download ts");
    this.fileService.getProcessedFiles().subscribe((data) => {

      this.blob = new Blob([data as BlobPart], {type: 'application/zip'});
      var downloadURL = window.URL.createObjectURL(data);
      var link = document.createElement('a');
      link.href = downloadURL;
      link.download = "a.zip";
      link.click();
    });
  }
}
